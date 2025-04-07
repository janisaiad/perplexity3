#!/usr/bin/env python3
import json
import re
import csv
import sys

def load_file_sections(filepath: str):
    """
    Lit le fichier et découpe le contenu en trois sections à partir des marqueurs :
    "Trade History:", "Activities log:" et "Sandbox logs:".
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    trade_history_marker = "Trade History:"
    activities_log_marker = "Activities log:"
    sandbox_logs_marker = "Sandbox logs:"

    # Découpage par marqueurs
    _, _, rest = content.partition(trade_history_marker)
    trade_history_section, _, rest = rest.partition(activities_log_marker)
    activities_section, _, sandbox_section = rest.partition(sandbox_logs_marker)
    return trade_history_section.strip(), activities_section.strip(), sandbox_section.strip()

def parse_trade_history(section: str):
    """
    La section Trade History est attendue sous la forme d'un tableau JSON.
    On le charge et retourne la liste d'objets.
    """
    try:
        history = json.loads(section)
        if isinstance(history, list):
            return history
        else:
            return []
    except Exception as e:
        print("Erreur lors du parsing de Trade History:", e)
        return []

def parse_activities_log(section: str):
    """
    La section Activities log est au format CSV avec un séparateur ";".
    On utilise la première ligne comme entête et on retourne une liste de dictionnaires.
    """
    lines = section.splitlines()
    if not lines:
        return []
    reader = csv.DictReader(lines, delimiter=";")
    activities = []
    for row in reader:
        try:
            row["timestamp"] = int(row["timestamp"])
        except:
            row["timestamp"] = None
        activities.append(row)
    return activities

def parse_sandbox_logs(section: str):
    """
    La section Sandbox logs contient plusieurs objets JSON.
    On utilise une expression régulière pour extraire chaque bloc JSON et on les charge.
    """
    json_blocks = re.findall(r"\{(?:.|\n)*?\}", section)
    sandbox_logs = []
    for block in json_blocks:
        try:
            data = json.loads(block)
            sandbox_logs.append(data)
        except Exception:
            continue
    return sandbox_logs

def merge_sections(trade_history, activities, sandbox_logs):
    """
    Fusionne les trois types d'informations en utilisant le timestamp comme clé unique.
    Pour chaque timestamp, on regroupe :
      - tradeHistory : liste des transactions,
      - activitiesLog : liste des lignes d'activité,
      - sandboxLogs : liste des logs sandbox.
    Retourne une liste d'objets triés par timestamp.
    """
    merged = {}
    # Fusion des transactions Trade History
    for entry in trade_history:
        ts = entry.get("timestamp")
        if ts is None:
            continue
        if ts not in merged:
            merged[ts] = {"timestamp": ts, "tradeHistory": [], "activitiesLog": [], "sandboxLogs": []}
        merged[ts]["tradeHistory"].append(entry)
    # Fusion des lignes d'activités
    for entry in activities:
        ts = entry.get("timestamp")
        if ts is None:
            continue
        if ts not in merged:
            merged[ts] = {"timestamp": ts, "tradeHistory": [], "activitiesLog": [], "sandboxLogs": []}
        merged[ts]["activitiesLog"].append(entry)
    # Fusion des Sandbox logs
    for entry in sandbox_logs:
        ts = entry.get("timestamp")
        if ts is None:
            continue
        if ts not in merged:
            merged[ts] = {"timestamp": ts, "tradeHistory": [], "activitiesLog": [], "sandboxLogs": []}
        merged[ts]["sandboxLogs"].append(entry)
    # Retourne une liste d'objets triés par timestamp
    merged_list = [merged[ts] for ts in sorted(merged)]
    return merged_list

def main(input_filepath: str, output_filepath: str):
    trade_section, activities_section, sandbox_section = load_file_sections(input_filepath)
    trade_history = parse_trade_history(trade_section)
    activities = parse_activities_log(activities_section)
    sandbox_logs = parse_sandbox_logs(sandbox_section)
    merged_data = merge_sections(trade_history, activities, sandbox_logs)
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2)
    print(f"Mega fichier de logs créé : {output_filepath}")

if __name__ == "__main__":
    input_filepath = "log_files/T1/T1_V1.log"
    output_filepath = "log_files/T1/T1_V1_merged.json"
    main(input_filepath, output_filepath)

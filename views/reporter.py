import os, time

class Reporter:
    @staticmethod
    def generate_report(output_base, summary, errors, start_time, end_time):
        report_path = os.path.join(output_base, "extraction_report.html")
        duration = end_time - start_time

        html = []
        html.append("<html><head><meta charset='utf-8'><title>Rapport Extraction</title></head><body>")
        html.append("<h1>Rapport d'extraction Amazon.fr High-Tech</h1>")
        html.append(f"<p>Début : {time.ctime(start_time)}<br>Fin : {time.ctime(end_time)}<br>Durée : {duration:.2f} sec</p>")

        html.append("<h2>Résumé</h2><ul>")
        for k, v in summary.items():
            html.append(f"<li>{k}: {v}</li>")
        html.append("</ul>")

        html.append("<h2>Erreurs</h2>")
        if errors:
            html.append("<ul>")
            for e in errors:
                html.append(f"<li><pre>{e}</pre></li>")
            html.append("</ul>")
        else:
            html.append("<p>Aucune erreur.</p>")

        html.append("</body></html>")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
        print(f"Rapport généré : {report_path}")

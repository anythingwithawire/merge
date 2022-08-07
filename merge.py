#!/usr/bin/env python

import subprocess

# Dieses Skript dient dazu, eine Reihe von pdfs zu einem einzigen pdf zusammenzufassen und bookmarks fuer diese pdf-Datei zu erzeugen.
# Dafuer wird ein Datei pdfmark benoetigt, die mit diesem Skript erzeugt wird.
# Dazu einfach dieses Skript in dem Verzeichnis aufrufen, das genau alle zusammenzufassenden pdfs (*pdf, s.u.) enthaelt.
# Das zusammenfassende pdf wird dann mit diesem Befehl (in der bash) generiert:
# gs -dBATCH -dNOPAUSE -sPAPERSIZE=A4 -sDEVICE=pdfwrite -sOutputFile="all.pdf" $(ls *pdf ) pdfmarks
# Bereits Inhaltsverzeichnisse bleiben erhalten, die neuen kommen ans Ende des Inhaltsverzeichnisses.
#
# pdfmarks sieht dabei prinzipiell so aus:
#
# [/Title (Nr. 1) /Page 1 /OUT pdfmark
# [/Title (Nr. 2) /Page 5 /OUT pdfmark
# [/Title (Nr. 3) /Page 9 /OUT pdfmark
# usw.

p = subprocess.Popen('ls *pdf', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

pdfdateien = []
kombinationen = []

for line in p.stdout.readlines():
# p enthaelt alle pdf-Dateinamen
  pdfdateien.append(line)


for datei in pdfdateien:
  cmd = "pdfinfo %s" %datei 
  q=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  kombination = [datei]

for line in p.stdout.readlines():
# p enthaelt alle pdf-Dateinamen
  pdfdateien.append(line)


for datei in pdfdateien:
  cmd = "pdfinfo %s" %datei 
  q=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  kombination = [datei]


  for subline in q.stdout.readlines():
# q enthaelt die Zeilen von pdfinfo
    if "Pages" in subline:
      kombination.append(subline)

  kombinationen.append(kombination)


# Jetzt kombinationen in benoetigtes Format bringen:

kombinationen_bereinigt =  []
out_string1 = "[/Title ("
out_string2 = ") /Page "
out_string3 = " /OUT pdfmark\n"
seitenzahl = 1

for kombination in kombinationen:
  dateiname = kombination[0][0:len(kombination[0])-5]

#
# Hier noch dateiname evtl. verwursten
# z. B.
#  lesezeichen = dateiname[0:1]+" "+dateiname[6:8]+"/"+dateiname[1:5]
  lesezeichen = dateiname

  anz_seiten = kombination[1][16:len(kombination[1])-1]
  seitenzahl_str = str(seitenzahl)

  kombination_bereinigt = out_string1+lesezeichen+out_string2+seitenzahl_str+out_string3
  kombinationen_bereinigt.append(kombination_bereinigt)

  seitenzahl += int(anz_seiten)


# Ausgabe ins file
outfile = open("pdfmarks", "w")

for i in kombinationen_bereinigt:
  outfile.write(i)

outfile.close()

# Merge-Befehl absetzen

print "\nFor merging all pdfs execute this (or similar) command (in bash shell):"
print "gs -dBATCH -dNOPAUSE -sPAPERSIZE=A4 -sDEVICE=pdfwrite -sOutputFile=\"all.pdf\" $(ls *pdf ) pdfmarks\n"

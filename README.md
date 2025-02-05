### SSL Automatisch rooster.

## Hoe gebruik je dit
Zorg ervoor dat je alle python libraries hebt die in requirements.txt staan.

In de map "input" moeten de volgende dingen staan:
<ul>
  <li><strong>planning_leeg.html</strong> Hier hoef je (waarschijnlijk) niet aan te zitten.</li>
  <li><strong>cursusplanning.csv</strong> Hier kan je je planning in maken, check de templates in de "templates" map.</li>
  <li><strong>opgavenlijst_tweedaags.csv of opgavenlijst_driedaags.csv</strong> Hierin maak je je opgavenlijstjes. Deze mogen blijven staan, ook als je een planning wil maken voor een anderdaagse cursus.</li>
  <li><strong>praktisch.html</strong> Hier in maak je wat in het onderdeel "praktisch" komt te staan.</li>
</ul>

Hierna kan je build_html_planning.py runnen.

## presentatierooster2csv
In deze map zit een script dat automatisch je presentatierooster inleest en verandert in een (niet compleet ingevuld) csv bestand dat build_html_planning.py kan lezen. Om dit te gebruiken plaats je een presentatierooster.xlsx bestand in dezelfde map. Verander de constanten bovenin het script naar wens.

## timeline
In deze map zit oude code voor het genereren van de timeline. Wordt niet gebruikt

## Wat mist nog?
Dit staat niet perse op de planning.
<ul>
  <li>Ondersteuning voor herkansingscursussen.</li>
  <li>Automatische kleuring bij meerdere docenten.</li>
  <li>Tekenen van observaties.</li>
  <li>Tekenen van trainingen.</li>
</ul>

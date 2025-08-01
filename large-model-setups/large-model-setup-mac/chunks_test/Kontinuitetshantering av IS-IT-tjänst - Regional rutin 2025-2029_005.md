| Driftskontinuitet                     | Konfiguration, övervakning, underhåll och administration av hårdvara, programvara och nätverk för att säkerställa kontinuerlig drift av IS/IT-tjänst.                   |
|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IS/IT-tjänst                          | Är en avgränsning av en eller flera digitala informationsbehandlingsresurser. Exempelvis IT-system, applikation, mjukvara, nätverk, lagringssystem eller infrastruktur. |
| Kontinuitet för informationssäkerhet  | Processer och rutiner som säkerställer att informationssäkerheten upprätthålls                                                                                          |
| Kontinuitetshantering                 | Innebär att planera för att upprätthålla sin verksamhet på en tolerabel nivå när den utsätts för en störning.                                                           |
| Kontinuitetshantering av IS/IT-tjänst | Innebär att planera för, förebygga och hantera störningar så att tillgängligheten kan upprätthållas.                                                                    |
| Kontinuitetsplan                      | En kontinuitetsplan för IS/IT-tjänst innehåller plan för förebyggande åtgärder och åtgärder vid en störning så att alla vet                                             |
vad som ska göras. Kallades tidigare avbrottsplan. Kallas i ISO 27002 IKT- kontinuitetsplan.
Redundans
Tillstånd då mer än ett medel finns för att upprätthålla ett givet funktionssätt syftande till att säkerställa kontinuerlig drift och därigenom öka feltoleransen. Dubbel eller flerfaldig uppsättning av viktiga komponenter för att IS/IT-tjänst ska fungera även om något slutar fungera.
## 4 Ansvar och roller
##  Ägare av IS/IT-tjänst
Ägare av IS/IT-tjänst ansvarar för att säkra kraven på kontinuitet i sin tjänst utifrån de krav som verksamheten har. Ägare av IS/ITtjänst ansvarar för att kontinuitetsplan för IS/IT-tjänst tas fram.
##  Informationsägare
Informationsägare ansvarar för att kravställa på tillgänglighet och kontinuitetshantering av IS/IT-tjänst.
Informationsägare ansvarar för att verksamhetens kontinuitetsplan och kontinuitetshantering av berörda IS/ITtjänster harmoniserar med varandra.
##  Regional processägare
För regionala processer företräder regional processägare informationsägare och ansvarar för att kravställa på tillgänglighet och kontinuitetshantering av regionala IS/IT-tjänster.
## 5 Kontinuitetshantering av IS/IT-tjänst
Kontinuitetshantering av IS/IT-tjänst innebär att planera för, förebygga och hantera störningar så att tillgängligheten kan upprätthållas. Hur långt man ska gå i kontinuitetshantering av respektive tjänst avgörs av verksamhetens krav uttryckta som tillgänglighet i informationsklassningen samt om IS/IT-tjänsten ingår som förutsättning för upprätthållande av en samhällsviktig verksamhet.
Kontinuitet för verksamhet styrs av Kontinuitet - Regional riktlinje 2023 -2027.
##  När ska en kontinuitetsplan tas fram?
Med kontinuitetsplanering avses den planering som behövs för att minimera de negativa effekter som kan bli resultatet av olika typer av avbrott i tillgång till informationen.
En kontinuitetsplan ska utvecklas och upprätthållas för varje IS/IT-tjänst där verksamheten kravställer och prioriterar kontinuitet. Minst de delar av IT-miljö som hanterar information med konsekvensnivå allvarlig (3) för tillgänglighet alternativt används för att tillhandahålla samhällsviktiga tjänster, enligt NISdirektivet och §14 i Lag (2018:1174) om informationssäkerhet för samhällsviktiga och digitala tjänster, ska omfattas fullt ut av rutinen. Kontinuitetsplan ska finnas innan installation eller ändringshantering av IS/IT-tjänsten enligt Change Management.
##  Vad ska en kontinuitetsplan innehålla?
Kontinuitetsplanen utgår från konsekvensanalys som genomförs inom ramen för verksamhetens kontinuitetshantering samt informationsklassningens krav på tillgänglighet. För verksamhetens kontinuitet ansvarar ytterst förvaltnings- eller bolagschef i enlighet med Kontinuitet - Regional riktlinje 2023 -2027.
Förvaltningar och bolag ska enligt Kontinuitet - Regional riktlinje 2023 -2027 identifiera sin lägsta nivå av riskacceptans och maximal tolerabel avbrottstid (MTA). Tillsammans med informationsklassning utgör de underlag för plan för kontinuitetshantering av IS/IT-tjänst.
Ägare IS/IT-tjänst ansvarar för att kontinuitetsplan för IS/ITtjänst tas fram. Planen ska inkludera förebyggande åtgärder utifrån risk, incidenthantering, arbetsrutiner och mål för återställning och återgång samt kontaktlista för kommunikation och beslut. Planen omfattar åtgärder runt driftskontinuitet, redundans, backup och reservkapacitet som implementeras i syfte att minska störningar och säkerställa klassad nivå av tillgänglighet. Planen ska hänvisa till verksamheternas MTA och informationsklassning. Planen bör uttrycka Recovery Time Objective (RTO), som innebär maxtid för återställning av IS/ITtjänst efter avbrott, och Recovery Point Objective (RPO), som
uttrycker hur långt tillbaka data maximalt får förloras vid avbrott av IS/IT-tjänsten.
Planen ska omfatta upprätthållande av informationssäkerhet under störning genom tillämpning av ISO/IEC 27002, avsnitt  och åtgärder för redundans ska säkerställa tillämpning av ISO/IEC 27002, avsnitt .
##  Återställning och återgång
Det ska i kontinuitetsplan för IS/IT-tjänst finnas utarbetade planer för hur IS/IT-tjänst återställs efter avbrott. Roller och ansvar, återställningstid och rutin för återställning ska vara tydligt definierade för att genomföra återställning och verifiera återgång till normalläge.
##  Riskhantering
Kontinuerlig riskhantering och sårbarhetshantering ska ske enligt respektive regional rutin för att identifiera potentiella hot och sårbarheter i IT-infrastrukturen, vilka kan påverka kontinuerlig drift. Se Regional rutin riskhantering för informationssäkerhet 2024 -2028 samt Regional rutin för hantering av sårbarheter i IT-miljö 2024 -2028. Resultatet ska användas för att prioritera och justera åtgärder i kontinuitetsplanen för att minska riskerna.
##  Incidenthantering
Incidenthantering ska ske enligt regional rutin incidenthantering.
Ägare IS/IT-tjänst ansvarar för att kontinuitetsplaner löpande förbättras när ny kunskap tillkommer. Kontinuitetplaner ska uppdateras regelbundet eller vid incidenter som har eller kan få en avsevärd påverkan på kontinuitet i IS/IT-tjänst. Sådana incidenter måste också rapporteras enligt lag för verksamheter som omfattas, till exempel hälso- och sjukvård genom lag (NIS2-direktivet) och direktivet om kritiska entiteters motståndskraft (CER-direktivet). Incidenter med IS/IT tjänster som är medicintekniska produkter eller som påverkar medicintekniska produkter måste bedömas om de också ska anmälas till tillverkaren och Läkemedelsverket som en händelse eller tillbud med en medicinteknisk produkt (HSLFFS 20221:52).
Koncernstab digitalisering (KSD) ska följa gällande incidenthanteringsprocess för att rapportera, utreda och hantera störningar och incidenter som kan påverka IS/IT-tjänster. Det
säkerställer en tydlig och koordinerad respons vid störningar enligt kontinuitetsplan.

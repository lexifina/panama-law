# Estructura / Structure

| Carpeta | Contenido |
| --- | --- |
| `constitucion/` | La Constitución Política de la República de Panamá (Texto Único de 2004, edición de 2024) |
| `codigos/<codigo>/` | Códigos: `codigos/codigo-penal/`, `codigos/codigo-procesal-penal/`, `codigos/codigo-del-trabajo/`, ... |
| `leyes/<año>/<NNNN>-<objeto>/` | Leyes de la Asamblea Nacional, por año y número, p. ej. `leyes/2011/0003-regula-participacion-padres-familia-acudientes-proceso/` |
| `decretos-ley/<año>/…`, `decretos-de-gabinete/<año>/…` | Decretos Leyes y Decretos de Gabinete |
| `decretos-ejecutivos/<año>/…`, `decretos/<año>/…`, `reglamentos/<año>/…` | Decretos Ejecutivos, Decretos y Reglamentos del Órgano Ejecutivo |
| `actos-legislativos/<año>/…`, `textos-unicos/<año>/…` | Actos legislativos (reformas constitucionales) y Textos Únicos |

Cada carpeta de norma tiene un archivo por artículo (`art-012.md` es el artículo 12; `art-012-a.md` el 12-A),
`encabezado.md` (lo anterior al artículo 1), `firma.md` (la fórmula de cierre y las firmas) y un `README.md`. Un
instrumento aprobado con numeración propia (un convenio, un reglamento anexo) queda en `anexo-1/`, `anexo-2/`, …. Una
norma sin artículos queda en `texto.md`. Ninguna carpeta tiene más de 1.000 entradas.

## Fechas / Dates

Each norm is one commit, as promulgated, dated 12:00 America/Panama on the day it took effect, repeated in its
`In-force:` trailer; `In-force-basis:` quotes the norm's own entry-into-force clause, counted from its promulgation in
the Gaceta Oficial (`Published:`). Norms with no such clause, or one that cannot be dated, are held, not guessed.
Norms in force before 1970 are stamped 1970-01-01, with the real day in the subject and the `In-force:` trailer. No
date in this repository is the day we downloaded anything.

## Fuentes / Sources

Legispan (Asamblea Nacional de Panamá): the text it extracts from each norm's PDF. Text read from a scan's own OCR
layer carries `Text-source: publisher OCR` (we do no OCR ourselves). The Constitution, the Código Penal, the Código
Procesal Penal and the Código del Trabajo come from the editions named in README.md.

## Ahora / Now

789 norms: leyes 789; 3 codes. 12 added by the runner (0 with the publisher's OCR layer; 9 with later amending norms listed in their README); 1917-06-18 to 1973-01-25.

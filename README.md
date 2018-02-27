# Ejercicio 1

## Basic Statistics
================
sents: 17378
tokens: 517194
words: 46501
tags: 85

## Most Frequent POS Tags
======================
| tag     | freq               | %    | top                                       | 
|---------|--------------------|------|-------------------------------------------| 
| sp000   | 939.8117647058823  | 0.18 | (de, en, a, del, con)                     | 
| nc0s000 | 746.4941176470588  | 0.14 | (presidente, equipo, partido, país, año)  | 
| da0000  | 641.7529411764706  | 0.12 | (la, el, los, las, El)                    | 
| aq0000  | 398.8941176470588  | 0.08 | (pasado, gran, mayor, nuevo, próximo)     | 
| fc      | 354.67058823529413 | 0.07 | (,)                                       | 
| np00000 | 342.4823529411765  | 0.07 | (Gobierno, España, PP, Barcelona, Madrid) | 
| nc0p000 | 326.3058823529412  | 0.06 | (años, millones, personas, países, días)  | 
| fp      | 206.0235294117647  | 0.04 | (.)                                       | 
| rg      | 180.42352941176472 | 0.03 | (más, hoy, también, ayer, ya)             | 
| cc      | 176.74117647058824 | 0.03 | (y, pero, o, Pero, e)                     | 



## Word Ambiguity Levels
=====================
| n | words | %     | top                                                     | 
|---|-------|-------|---------------------------------------------------------| 
| 1 | 51    | 0.11  | (,, ., y, ", a)                                         | 
| 2 | 266   | 0.57  | (de, la, el, en, un)                                    | 
| 3 | 962   | 2.07  | (que, los, del, las, con)                               | 
| 4 | 1701  | 3.66  | (para, como, pero, años, este)                          | 
| 5 | 3225  | 6.94  | (entre, sobre, desde, hasta, tiene)                     | 
| 6 | 4260  | 9.16  | (porque, cuando, pasado, equipo, contra)                | 
| 7 | 5531  | 11.89 | (también, partido, durante, después, pesetas)           | 
| 8 | 5752  | 12.37 | (millones, Gobierno, política, ministro, personas)      | 
| 9 | 5353  | 11.51 | (Barcelona, situación, jugadores, problemas, electoral) | 


# Ejercicio 2

+ Accuracy: 12.65%

# Ejercicio 4

## Logistic Regression
### n = 1
+ Accuracy: 91.69%
+ Tiempo de ejecución: 27.325s

### n = 2
+ Accuracy: 91.26%
+ Tiempo de ejecución: 27.238s

### n = 3
+ Accuracy: 91.59%
+ Tiempo de ejecución: 27.897s

### n = 4
+ Accuracy: 91.70%
+ Tiempo de ejecución: 27.527s

## Multinomial
### n = 1
+ Accuracy: 77.17%
+ Tiempo de ejecución: 78m 30.528s

### n = 2
+ Accuracy: 75.05%
+ Tiempo de ejecución: 79m 31.688s

### n = 3
+ Accuracy: 74.92%
+ Tiempo de ejecución: 84m 14.533s

### n = 4
+ Accuracy: 74.07%
+ Tiempo de ejecución: 84m 16.752s

## SVM
### n = 1
+ Accuracy: 94.11%
+ Tiempo de ejecución: 30.876s

### n = 2
+ Accuracy: 94.05%
+ Tiempo de ejecución: 31.148s

### n = 3
+ Accuracy: 94.25%
+ Tiempo de ejecución: 31.504s

### n = 4
+ Accuracy: 94.25%
+ Tiempo de ejecución: 31.612s
# NOTA
Por una cuestión de tamaños de archivos, los modelos entrenados no están subidos al repo. De necesitarlos, se encuentran en: https://drive.google.com/drive/folders/1oV57LS2_DZXb65voC9s2ZgdFIjKfNSVy?usp=sharing


Word Ambiguity Levels
=====================
n words % top
1 43972 94.56 (,, con, por, su, El)
2 2318  4.98  (el, en, y, ", los)
3 180 0.39  (de, la, ., un, no)
4 23  0.05  (que, a, dos, este, fue)
5 5 0.01  (mismo, cinco, medio, ocho, vista)
6 3 0.01  (una, como, uno)
7 0 0.00  ()
8 0 0.00  ()
9 0 0.00  ()


## Basic Statistics
================
sents: 17378
tokens: 517194
words: 46501
tags: 85

## Most Frequent POS Tags
======================
| tag     | freq               | %     | top                                       | 
|---------|--------------------|-------|-------------------------------------------| 
| sp000   | 79884              | 15.45 | (de, en, a, del, con)                     | 
| nc0s000 | 63452              | 12.27 | (presidente, equipo, partido, país, año)  | 
| da0000  | 54549              | 10.55 | (la, el, los, las, El)                    | 
| aq0000  | 33906              | 6.56  | (pasado, gran, mayor, nuevo, próximo)     | 
| fc      | 30147              | 5.83  | (,)                                       | 
| np00000 | 29111              | 5.63  | (Gobierno, España, PP, Barcelona, Madrid) | 
| nc0p000 | 27736              | 5.36  | (años, millones, personas, países, días)  | 
| fp      | 17512              | 3.39  | (.)                                       | 
| rg      | 15336              | 2.97  | (más, hoy, también, ayer, ya)             | 
| cc      | 15023              | 2.90  | (y, pero, o, Pero, e)                     | 



## Word Ambiguity Levels
=====================
| n | words | %     | top                                | 
|---|-------|-------|------------------------------------| 
| 1 | 43972 | 94.56 | (,, con, por, su, El)              | 
| 2 | 2318  | 4.98  | (el, en, y, ", los)                | 
| 3 | 180   | 0.39  | (de, la, ., un, no)                | 
| 4 | 23    | 0.05  | (que, a, dos, este, fue)           | 
| 5 | 5     | 0.01  | (mismo, cinco, medio, ocho, vista) | 
| 6 | 3     | 0.01  | (una, como, uno)                   | 
| 7 | 0     | 0.00  | ()                                 | 
| 8 | 0     | 0.00  | ()                                 | 
| 9 | 0     | 0.00  | ()                                 | 


# Ejercicio 2

+ Accuracy: 87.58%

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
# Lexer-Python

Lexerul primeste o specificatie de tokens ce contine expresii regulate.

Fisierul va contine un token si expresia lui regulata, cate una pe fiecare linie, sub urmatoarea forma:
```
<token> <regex>;
```

Implementarea lexerului complet presupune:
1. Citirea si parsarea specificatiei
2. Generarea de AFD-uri
3. Implementarea procedurii de analiza lexicala

Transformarea Regex-AFD permite operationalizarea expresiilor regulate si este realizata in doi pasi:
- transformarea Regex → AFN
- transformarea AFN → AFD

# Key Exchange
Con il termine *key ecxchange* si fa riferimento ad un algoritmo particolare: **Diffie-Hellman (DH)**. Questo permette lo scambio di un segreto condiviso come una chiave privata simmetrica su un canale insicuro. Bisogna però differenziare le garanzie di sicurezza in base al *threat modelling*:
* MITM (Man-in-the-Middle) passivo (***eavesdropping***): basta un **unauthenticated** DH
* MITM (Man-in-the-Middle) attivo: è necessario un **authenticated** DH, in quanto basterebbe all'attore malevolo *Eve* eseguire un doppio scambio con gli attori validi (*Alice* e *Bob*) per poter intromettersi nella loro comunicazione.

## Un po' di matematica
Importanza dei numeri **primi**

  => le librerie moderne non cercano numeri primi, ma *pseudo-primi* (per fattori legati alle performance), controllano se la probabilità di un numero di non essere primo è inferiore ad una certa *threeshold*: ***Miller-Rabin primality test***

Questo porta a problematiche legate ad inesattezze di questi algoritmi => 2017. [ROCA vulnerabilities](https://en.wikipedia.org/wiki/ROCA_vulnerability).

## Diffie-Hellman (DH)
Si basa sul problema del [***Discrete logarithm problem (DLP)***](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm). Nella crittografia asimmetrica ci sono due diversi contributi:
* privato: per DH è $a \in \mathbb{Z}_p$
* pubblico: per DH è $g^a \text{ mod } p$

Dove $p$ è un primo molto grande e $g$ è un generatore di $\mathbb{Z}_p$. Per calcolare l'esponenziazione modulare c'è una tecnica chiamata **Square and Multiply** che permette di calcolare in maniera efficente $g^a$ andando ad iterare bit a bit $a$.

Garanzie di sicurezza di DH:
* **Computational Diffie-Hellman (CDH)**: dati $g^a$ e $g^b$ non si può calcolare $g^{ab}$
* **Decisional Diffie-Hellman (DDH)**: osservato su un canale insicuro un valore $k$ è "impossibile" distinguerlo da un valore random o dal contributo pubblico ($g^a$ o $g^b$)

Due versioni di DH: [**Finite Field Diffie-Hellman (FFDH)**](https://www.rfc-editor.org/info/rfc7919/) e **Elliptic Curve Diffie-Hellman (ECDH)**

Gestione della lunghezza delle chiavi per garantire almeno 128 bits di sicurezza. [link](https://www.keylength.com/). Come generatore di solito viene scelto $g=2$ perché permette di utilizzare il *left shift* (<<) come operazione.

Nel 2016 **socat** non utilizzava un numero primo per DH, rendendo più semplice per gli attaccanti ottenere il segreto condiviso. [CVE-2016-2217](https://www.cve.org/CVERecord?id=CVE-2016-2217)

## Elliptic Curve (EC)
Forma generale: $y^2 +a_1xy + a_3y = x^3 + a_2x^2 + a_4x + a_6$. 

Normalmente si predilige la **forma di weierstrass**: $y^2 = x^3 + ax + b$, non è sempre possibile semplificare la formula. Le tipologie di curve non semplificabili sono:
* *binary curves*
* *curver of characteristic 3*

Garanzia di sicurezza di ECDH è il **Elliptic Curve Discrete Logarithm Problem (ECDLP)**, dove si assume che sia computazionalmente oneroso, dato $P = [x]G$ trovare lo scalare $[x]$ utilizzato per trovare il punto $P$.

L'attacco più forte a DH è [**index calculus**](https://en.wikipedia.org/wiki/Index_calculus_algorithm) (anche noto come: **number field sieve attack**) non è ottimizzato per le curve ellittiche.

Esistono varie curve standardizzate, ma per paura che NSA avesse inserito delle backdoor su certe curve oggi ne vengono utilizzate solo due:
* P-256 (secp256r1) 
* [Curve25519](https://en.wikipedia.org/wiki/Curve25519) anche nota come **Montgomery curve** (x25519)

Entrambe sono a 128 bit di sicurezza (quindi il primo è a 256 bit), se si vuole aumentare i bit di sicurezza e quindi aumentare la lunghezza del primo utilizzato a 512 bit bisogna utilizzare P-251 (si avranno quindi 256 bit sicurezza).

[RFC 5114](https://www.rfc-editor.org/info/rfc5114/) è associato ad una serie di vulnerabilità dovute all'utilizzo di *non-safe primes* che possono portare a utilizzo di *small groups* e quindi a eseguire l'ECDLP attraverso l'algoritmo di: [**Pohlig-Hellman**](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm) in modo da ottimizzare la computazione.

## Security Considerations
* *safe (strong) primes* $p = 2q + 1$ dove $q$ è anchesso un primo, permettono di evitare attacchi a *small subgroup*. => **least significant leakge*: Eve invia come contributo pubblico $g^b = -1$, se il valore di ritorno $1$ allora il contributo privato di Alice è pari, se invece il valore di ritorno è $-1$ allora il contributo privato di Alice è dispari.
* EC non hanno *small subgroup* ad eccezione di quello di ordine 1 (dove l'unico elemento è il punto all'**infinito** $\mathcal{O}$ => **invalid curve attack**, Eve invia un punto che non appartiene alla curva scelta per la comunicazione. **Always check the pk belongs on the Curve**

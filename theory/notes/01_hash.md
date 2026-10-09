# Hash Functions
Alcune applicazioni delle hash functions:
* commitments
* *subresource integrity*: quando una pagina web importa un js esterno da una CDN può validare il file utilizzando un digest

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" 
        integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz"</script>
```
* BitTorrent
* Tor (URLs): troncando il digest
* hashing password (Argo2 + salting aumentano il tempo di brute force dell'hash)

#### hash functions != error detecting code functions

## Standard hash functions

MD5 e SHA-1 sono deprecate perché la sicurezza della CR (collision resistance) è stata violata, ma sono ancora utilizzate perché in alcune applicazioni quel vincolo di sicurezza non è necessario ed è quindi sufficente che garantiscano PR (pre-image collision resistance) e 2PR (second pre-image collision resistance), cosa che MD5 e SHA-1 possono ancora garantire.

SHA-2 utilizza la costruzione di Merkle-Damgard dove la *compression function* è costruita attraverso il metodo di Davies-Meyer che poggia le sue basi sui block cipher. A differenza di SHA-3 (Keccak) che utilizza costruzione SPONGE che non è vulnerabile a *length-extension attack*.SHA-3 è costruita sulla funzione di permutazione ***keccak-f***.

La costruzione è chiamata SPONGE perché è costituita da due parti:
* absorbing: permette di innestare nello stato interno della funzione di hash, l'input
* squeezing: che permette di creare il digest vero e proprio

Lo stato interno in Keccak viene inizializzato a 0 e viene diviso in due parti *rate* (*r*) e *capacity* (*c*); l'input va ad influire direttamente sul *rate*, mentre la *capacity* rimane "nascosta". La *capacity* è l'elemento che garantisce la sicurezza crittografica della funzione:
* CR -> `pow( 2, c // 2 )`
* PR -> `pow(2, c)` o lunghezza *n* nell'input

## Extendable output functions (XOF)
Alcuni utilizzi delle XOF:
* creazione di numeri random
* derivazione delle chiavi

Permettono di decidere arbitrariamente la lunghezza del digest: SHAKE e cSHAKE. La differenza tra le due è che in cSHAKE è possibile inserire una `custom_string` che non è parte del dato di cui calcolare il digest, ma che lo influisce. Questo meccanismo permette quello che viene definito ***domain separation***. In crittografia è buona norma che se la stessa primitiva crittografica viene utilizzata per obiettivi differenti (algoritmo per garantire confidenzialità e per garantire autenticazione) non utilizzino la stessa chiave, se è presente una chiave, o/e sia possibile applicare la *domain separation*.

### TupleHash
Permette di evitare ambiguità nella creazione di hash di testo serializzato. Durante una concatenzaione (serializzazione) di più informazioni è possibile andare ad alterare i valori dei singoli campi senza campiarne l'hash.


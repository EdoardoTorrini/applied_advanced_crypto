# Message Authentication Code (MAC)
`t = MAC(key, message)` dove l'output è chiamato anche *tag*.

## Security Properties
* non deve essere possibile fare ***authentication tag forgery***, ovvero non deve essere possibile creare un *tag* valido dato un messaggio arbitrario
* le funzioni MAC devono essere ***collision resistance*** quindi è importante valutare la lunghezza del *tag*, a differenza degli hash che sono algoritmi facilmente eseguibili offline, il MAC per essere generato prevede una query ad un oracolo, quindi la lunghezza del MAC può essere la metà di quello di un hash in quanto i bit di sicurezza si dimezzano ma il tempo impiegato per una computazione è da considerarsi online => 128 bit di lunghezza del MAC sono sufficenti
* ***replay attack***, possono essere arginabili tramite dei contatori => i counter non devono essere a lunghezza variabile. `MAC("1" || "1 is my favorite number") = MAC("11" || " is my favorite number")`
* la verifica del tag di autenticazione deve essere fatto in *constant time*

## Use Cases
* **message authentication**
* **deriving key**: HKDF (basata su HMAC), non tutti i MAC sono delle PRF => `MAC(key, message) || 0x01` 
* **integrity of cookies**
* **hash table**: se un servizio espone un hash table un attore malevolo può causare un denial of service sull'hash table, è possibile utilizzare un MAC per evitare questo tipo di problemi => **SipHash**: ottimizzato in modo tale da avere un tag corto
* **RNG** (random number generator): permette di generare dei numeri random in maniera deterministica (TOTP utilizza questa tecnologia)

## Tipologie di MAC - maggiormente utilizzare
* **HMAC**: basati sugli hash `HASH( k ^ opad || HASH( k ^ ipad || message ) )`
* **KMAC**: basati su cSHAKE, utilizza di default la `custom_string = "KMAC"`. si può modificare sia `custom_string` che la lunghezza del *tag* in questa tipologia id MAC

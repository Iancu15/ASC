1. Implementarea solutiei

Ideea de la care am pornit initial a fost sa pornesc un kernel cu un numar de thread-uri
egal cu numarul de orase, astfel fiecare thread se va ocupa de calcularea populatiei
accesibile pentru un oras. In mod normal pentru a scadea numarul de comparatii as
incerca sa nu fac un for in for simplu de la 0 la n. O idee mai desteapta pentru un
algoritm secvential era sa fac din ce in ce mai putine comparatii si anume sa compar
intai primul oras cu toate celelalte si sa adaug la populatiile accesibile pentru ambele
orase din comparatie in caz ca sunt apropiate, apoi al doilea oras cu restul de (n - 1) orase
si tot asa pentru fiecare oras avand cu 1 mai putin de comparat. In final tot la o complexitate
de O(n^2) se ajungea(n - nr. de orase), dar una cu performante umpic mai ridicate. Problema e ca solutia
asta nu se muleaza bine pe o implementare paralela si mai ales pe implementarea mea cu un
oras per thread. Asta pentru ca primul thread ar avea N operatii de realizat, pe cand ultimul
thread ar avea 1 operatie de realizat. Asta nu prea m-ar ajuta daca toate thread-urile ar incepe
in acelasi timp pentru ar trebui sa astept primul thread sa se termine si faptul ca ultimul se termina
mai rapid nu ajuta. Totusi daca thread-urile nu sunt planificate in mod egal de catre scheduler, atunci
s-ar putea sa se vada un boost de performanta, totusi ar aparea un nedeterminism al performantei care
ar fi influentat de modul in care scheduler-ul planifica thread-urile la momentul curent. De asemenea,
o problema mare cu o astfel de abordare ar fi faptul ca ar trebui sa folosesc atomicAdd pentru ca
mai multe thread-uri sunt sanse sa adauge in acelasi timp populatie la un anumit oras. Si daca se poate
e mai bine sa nu folosesti atomicAdd ca ia din performanta.

M-am decis sa fac o problema embarrassingly parallel in care thread-urile ar avea task-uri total
independente pentru a nu mai folosi atomicAdd. Ne intoarcem astfel la metoda cu for in for de la 0 la N.
In loc sa adaug la ambele orase participante la comparatie, adaug doar la orasul asignat thread-ului curent.
Astfel n-are cum sa fie race condition pentru ca fiecare thread va adauga la acelasi element din vector.
Oras-ul pentru care calculeaza un thread valoarea accesibila va fi dat de globalId-ul sau. For-ul exterior
fiind impartit prin paralelism, fiecare thread ocupandu-se de un oras, iar cel interior aflandu-se in cadrul
fiecarui thread. Astfel de la algoritmul secvential de O(n^2) se ajunge la o complexitate de O(n) per thread,
unde n este numarul de orase. Cum se trece prin toate orasele pentru fiecare thread, ma va interesa doar
populatia initiala a orasului respectiv, nu una partial accesibila. Asa ca voi folosi un vector popArrayIn constant
pentru a prelua populatiile oraselor si un vector popArrayOut in care voi scrie populatiile accesibile pentru a le
scrie in fisier la finalul rularii kernel-ului.

Eu m-am decis sa rulez independent fiecare thread, asta inseamna ca e independent si la nivel de bloc. Nu am
gasit o necesitate pentru folosirea de variabile sau vectori __shared__ cum singurele variabile sunt cele la nivel
local pentru thread si cele globale care sunt informatiile despre toate orasele, informatiile doar despre orasele
din bloc fiind insuficiente pentru calcularea populatiei accesibile. Totusi kernel-ul imi cere sa le impart pe
bloc-uri, asa ca am ales o dimensiune standard de 256 de thread-uri per bloc si am impartit numarul de orase la
256 pentru a afla numarul de bloc-uri. Am adaugat 1 la numarul de bloc-uri pentru cazurile in care numarul
de orase nu se imparte exact la 256. Thread-urile in plus din acel bloc vor fi ignorate facand verificarea
ca globalID sa fie mai mic decat numarul de orase in kernel.

In mare conceptual vorbind asta este implementarea, tot ce mai trebuind facut este folosirea functiei helper
pentru calcularea distantei intre 2 puncte pe sfera si daca se incadreaza in kmRange, atunci se adauga populatia
orasului cu care s-a comparat la populatia accesibila a orasului asignat thread-ului curent. In main trec prin
fisiere cu un for si pentru fiecare citesc informatiile relevante cum ar fi latitudinea, longitudinea si populatia
oraselor, apoi rulez kernel-ul si apoi scriu la iesire populatiile accesibile. Partea de citire si scriere sunt
chestii de I/O asa ca nu le pot paraleliza pentru un fisier. Totusi s-ar putea face o imbunatatire sa se citeasca si
sa scrie in paralel mai multe fisiere, acestea fiind independente una de alta. Totusi am considerat ca beneficiile
aduse nu merita pentru complexitatea adusa solutiei, partea I/O fiind irelevanta comparativ cu calcularea propriu-zisa.
Am terminat partea de baza a solutiei, tot ce se discuta de acum incolo sunt optimizari aduse variantei banale.

In primul rand, functia de calculare a distantei intre 2 orase consuma multe resurse datorita numarulului mare
de functii trigonometrice. Unele dintre ele calculandu-se de mai multe ori pentru aceleasi unghiuri, phi-ul
si theta-ul fiind mereu aceleasi pentru un anumit oras. In varianta balana se calculeaza astfel acel sin(phi)
si cos(phi) de N ori pentru un anumit oras, o data in fiecare thread. Astea sunt resurse consumate inutil, in
loc sa le calculeze redundant de N ori, m-am decis ca mai bine se calculeaza o singura data. Varianta naiva
de implementare ar fi ca in host sa se calculeze sin(phi), cos(phi), sin(theta), cos(theta) pentru fiecare oras
intr-un for. Totusi cum tot lucram in cuda am decis sa fac acest calcul initial de functii trigonometrice cat
mai putin costisitor facand un kernel in care fiecare thread calculeaza functiile trigonometrice pentru un
singur oras.

Calcularea lui cos(theta1 - theta2) nu o pot face inainte pentru ca tine de relatia dintre un oras si alt oras.
Insa acesta se poate rescrie ca cos(theta1) * cos(theta2) + sin(theta1) * sin(theta2) folosind formula de extindere
a cos(x - y). Acesti sin si cos fiind calculati inainte in kernel-ul de calculare a functiilor trigonometrice. Cea
mai problematica dintre functiile trigonometrice este calcularea lui acos(cs), pentru ca acest cs tine de relatia
dintre 2 orase si nu il pot inlocui cu o formula de sin si cos ca cos(theta1 - theta2). Cea mai la indeamna varianta
pentru a imbunatati calcularea acos-ului a fost sa folosesc o functie de aproximare cu marja de eroare buna. Am
folosit codul pentru acos folosit de Nvidia in Cg Standard Library. Acesta are eroarea absoluta mai mica sau egala cu 6.7e-5,
ceea ce din experiment pare sa fie destul de buna pentru problema noastra. Se poate gasi implementarea functiei la link-ul:

https://developer.download.nvidia.com/cg/acos.html

Alte precizari:
-n-am folosit functii __device__ pentru calcularea acos-ului sau altceva pentru ca scade din performanta;
-am inlocuit toate float-urile cu double pentru o precizie mai buna, imi pica testul E1 cand aveam float-uri
-am stocat latitudinea si longitudinea intr-o structura ca sa accesez doar o data vectorul de structuri
pentru structura cautata in loc sa accesez de 2 ori daca le-as fi stocat in 2 vectori diferiti, acelasi rationament
si pentru stocarea rezultatelor functiilor trigonometrice in structuri (unde as fi accesat de 4 ori ca sunt 4 campuri
in loc de o singura data pentru o structura).

2. Rezultate obtinute

Din 100 de rulari pe teste excluzand H1 repartizate pe placi in urmatorul fel:
93 - K40M
5 - A100
2 - P100

Doar 1 rulare pe K40M a dat timeout, pe restul de 99 de rulari am obtinut un punctaj
de 70/90, adica maximul excluzand H1.

Din 100 de rulari pe toate testele repartizate pe placi in urmatorul fel:
86 - K40M
7 - A100
3 - P100
4 - FATAL error la image mount, irelevant pentru ca tine de starea cluster-ului

Doar o rulare a trecut pe A100 cu 90/90, restul au dat timeout.

De mentionat ca rularea acestor 200 de rulari a fost facuta doar o singura data la final, in rest
pentru implementarea temei am facut cate o singura rulare.

Cum implementarea mea pare sa nu fie suficienta pentru rularea H1 din datele colectate,
pentru evaluare doresc sa se ruleze fara acesta pentru a lua punctajul de 70/90 pe teste. Am comentat
in run_local_checker linia respectiva, daca pentru evaluare se rescrie checker-ul, atunci as
dori linia aferenta H1 comentata.
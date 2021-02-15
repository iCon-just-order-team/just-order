:- dynamic(prop/3).

%===========================
%	CONOSCENZA DERIVATA
%===========================

% Definizione di classe
prop(X, type, C) :-
    prop(S, subClassOf, C),
    prop(X, type, S).

% Definizione dei requisiti all'indietro
prop(A, requirement, C) :-
    prop(A, type, B),
    prop(B, requirement, C).

% Definizione degli ingredienti contenuti
prop(I, is_contained, P):-
    prop(P, requirement, I),
    prop(P, type, B),
    prop(B, subClassOf, ricetta).

prop(I, is_not_contained, P):-
    prop(P, type, Y),
    prop(Y, subClassOf, ricetta),
    prop(P, requirement, I),
    prop(Z, type, ingrediente),
    not(Z == I).

% Definisce se è possibile cucinare il piatto P
prop(P, not_available_items, X):-
    prop(P, requirement, X),
    prop(X, in_inventory, false).

% Mostra gli elementi nell'inventario
prop(I, in_inventory, true):-
    prop(I, type, ingrediente),
    prop(I, availability, Y),
    Y > 0.

prop(I, in_inventory, false):-
    prop(I, type, ingrediente),
    prop(I, availability, Y),
    Y=:=0.

%Definisce per chi non è il piatto
prop(P, is_not_for, M):-
    prop(P, requirement, I),
    prop(I, is_not_for, M).

% Definisce se il numero N di utenti possono accomdarsi ai tavoli
prop(posto, availability, N):-
	prop(tavolo, total, X),
    X >= N,
    not(prop(cameriere, availability, 0)).

%===========================
%			FATTI
%===========================

%=== Disponibilità TAVOLI ====
prop(tavolo, total, 10).
prop(tavolo, availability, 10).

%=== Disponibilità STAFF ====
prop(cameriero, subClassOf, staff).
prop(cuoco, subClassOf, staff).
prop(cameriere, availability, 4).
prop(cuoco, availability, 2).


%=== Disponibilità INGREDIENTI ====
prop(pomodoro, type, ingrediente).
prop(pomodoro, availability, 10).

prop(pasta, type, ingrediente).
prop(pasta, is_not_for, celiaco).
prop(pasta, availability, 10).

prop(tonno, type, ingrediente).
prop(tonno, is_not_for, vegetariano).
prop(tonno, is_not_for, vegano).
prop(tonno, availability, 7).

prop(burro, type, ingrediente).
prop(burro, is_not_for, intollerante_lattosio).
prop(burro, is_not_for, vegano).
prop(burro, availability, 5).

prop(zucchina, type, ingrediente).
prop(zucchina, availability, 0).

prop(uovo, type, ingrediente).
prop(uovo, is_not_for, vegano).
prop(uovo, availability, 1).

prop(guanciale, type, ingrediente).
prop(guanciale, is_not_for, vegetariano).
prop(guanciale, is_not_for, vegano).
prop(guanciale, availability, 0).

prop(pecorino, type, ingrediente).
prop(pecorino, is_not_for, intollerante_lattosio).
prop(pecorino, is_not_for, vegano).
prop(pecorino, availability, 1).

prop(cozza, type, ingrediente).
prop(cozza, is_not_for, vegetariano).
prop(cozza, is_not_for, vegano).
prop(cozza, availability, 1).

prop(vongola, type, ingrediente).
prop(vongola, is_not_for, vegetariano).
prop(vongola, is_not_for, vegano).
prop(vongola, availability, 2).

prop(gamberetto, type, ingrediente).
prop(gamberetto, is_not_for, vegetariano).
prop(gamberetto, is_not_for, vegano).
prop(gamberetto, availability, 8).

prop(prezzemolo, type, ingrediente).
prop(prezzemolo, availability, 20).

prop(farina, type, ingrediente).
prop(farina, is_not_for, celiaco).
prop(farina, availability, 3).

prop(fungo, type, ingrediente).
prop(fungo, availability, 10).

prop(riso, type, ingrediente).
prop(riso, is_not_for, celiaco).
prop(riso, availability, 3).

prop(polpo, type, ingrediente).
prop(polpo, is_not_for, vegetariano).
prop(polpo, is_not_for, vegano).
prop(polpo, availability, 3).


%=== PASTA ====
prop(pasta_ricetta, subClassOf, ricetta).
prop(pasta_ricetta, requirement, pasta).
%=== Pasta Pomodoro ====
prop(pasta_pomodoro, type, pasta_ricetta).
prop(pasta_pomodoro, requirement, pomodoro).
%=== Pasta Tonno ====
prop(pasta_tonno, type, pasta_ricetta).
prop(pasta_tonno, requirement, tonno).
%=== Carbonara ====
prop(carbonara, type, pasta_ricetta).
prop(carbonara, requirement, pecorino).
prop(carbonara, requirement, guanciale).
prop(carbonara, requirement, uovo).
%=== Scoglio ===
prop(scoglio, type, pasta_ricetta).
prop(scoglio, requirement, cozza).
prop(scoglio, requirement, vongola).
prop(scoglio, requirement, gamberetto).
prop(scoglio, requirement, prezzemolo).

%=== RISOTTO ===
prop(risotto, subClassOf, ricetta).
prop(risotto, requirement, riso).
prop(risotto, requirement, burro).
%=== Risotto Zucchine ===
prop(risotto_zucchine, type, risotto).
prop(risotto_zucchine, requirement, zucchina).
%=== Risotto Funghi ===
prop(risotto_funghi, type, risotto).
prop(risotto_funghi, requirement, fungo).

%=== Arancino ===
prop(street_food, subClassOf, ricetta).
prop(arancino, requirement, street_food).
prop(arancino, requirement, gamberetto).
prop(arancino, requirement, farina).
prop(arancino, requirement, uovo).

%=== Pepata cozze ===
prop(frutti_mare, subClassOf, ricetta).
prop(pepata, type, frutti_mare).
prop(pepata, requirement, cozza).
prop(pepata, requirement, prezzemolo).
prop(pepata, requirement, pomodoro).
%=== Zuppa vongole ===
prop(zuppa, type, frutti_mare).
prop(zuppa, requirement, vongola).
prop(zuppa, requirement, zucchina).
prop(zuppa, requirement, pomodoro).

%=== Polpo luciana ===
prop(secondi_mare, subClassOf, ricetta).
prop(polpo, type, secondi_mare).
prop(polpo, requirement, polpo).
prop(polpo, requirement, prezzemolo).

%=== Pollo funghi ===
prop(secondi_carne, subClassOf, ricetta).
prop(pollo, type, secondi_carne).
prop(pollo, requirement, pollo).
prop(pollo, requirement, fungo).
prop(pollo, requirement, pomodoro).
prop(pollo, requirement, burro).
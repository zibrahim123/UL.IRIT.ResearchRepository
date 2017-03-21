%% Construction de matrice affinite
%% mesure d'affinité gaussienne 
% s(xi,xj)=exp(-norm(xi-xj)^2/(2 sigma^2))


function Aff=CreateMatAff(Points)

[n,m]=size(Points);

% Calcul des distances en norme euclidienne
d=sqdist(Points',Points');

% Heuristique pour definir le parametre sigma du noyau gaussien
sigma=sqrt(max(max(d)))/(n^(1/m));

% construction de la matrice affinite
Aff=exp(-d/(2*sigma^2));



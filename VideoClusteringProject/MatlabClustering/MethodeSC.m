%%%%%%%%
%% Méthode SC suite
%%%%%%%%%%%

function IDX=MethodeSC(A,k)

%Nombre de données
n=size(A,1);

%Definition de la matrice D de normalisation
D=diag(sum(A));

%Normalisation de la matrice affinité A1
L=D^(-1)*A; %stochastique



%Determination des vecteurs propres M et valeurs propres N de L
%disp('calcul des valeurs propres :')
[M,N]=eig(L);


%on ordonne la matrice des vecteurs propres par ordre decroissant des
%valeurs propres
G=diag(N);
[G1,II]=sort(G);
W=M(:,II);




%on prend les k + gds vecteurs propres i.e ceux dont les valeurs propres sont les k + gdes 
%ou les + petites pour le Laplacien
X=zeros(n,k);
X(:,1:k)=W(:,end-k+1:end); % pour affinité gaussienne


%Determination de la matrice Y i.e normalisation des lignes[] de X
Y=zeros(n,k);
Y=normr(X); 


%Recherche des k centres les plus orthogonaux entre eux possible
Z=Y;T=[];T2=[];T3=[];IDX=zeros(n,1);

%disp('Recherche des centres')
T=[Z(1,:)];

for j=1:n
    if  (norm(T(1,:)-Z(j,:),'inf')>10^(-1)) & (norm(Z(j,:)-T(end,:),'inf')>10^(-1))
            T=[T;Z(j,:)];
    end
end
   

%disp('centres orhogonaux :')
T(1:k,:);
    
%En considerant chaque ligne de Y comme un point de IR^k, on les classe
%dans k clusters + coordonnees des centres via K-means algorithme 
if k~=1
    [IDX,C]=kmeans(Y,k,'start',T(1:k,:));%finition kmeans initialisé
end





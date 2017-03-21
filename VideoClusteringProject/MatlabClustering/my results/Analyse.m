clear all
close all

%% Chargement des donn�es 
Descriptors=importdata('DescriptorsList.txt');

Dataset=Descriptors.data(:,1:end);
[n,m]=size(Dataset);

MesFeatureVideo=importdata('Feature_Video.out');
MesFeatureAudio=importdata('Feature_Audio.out');
MesFeature = MesFeatureVideo*0.25+MesFeatureAudio*0.75;
clear MesFeatureVideo MesFeatureAudio
%% Nombre limite de classes
nblimit=50;

%DAudio = pdist2(Dataset(:,2:20),Dataset(:,2:20),'cityblock');
%DVideo = pdist2(Dataset(:,21:24),Dataset(:,21:24),'cityblock');
%% Methode Kmeans
Partition=zeros(n,nblimit);
sumd1=zeros(nblimit,1);
for k=2:nblimit
[Partition(:,k),C1,Res]=kmeans(Dataset(:,2:24),k,'distance','cityblock');
sumd1(k)=mean(Res);
end



%% Recherche du nombre de classes
DiffSum=diff(sumd1);
seuil=median(abs(DiffSum));
ii=find(abs(DiffSum) < seuil);

disp('Nbre de classes optimal')
nbopt=ii(1)-1

figure
hold on 
plot(sumd1)
plot(nbopt,sumd1(nbopt),'r*')
xlabel('Nbre de classes')
ylabel('Distance moyenne intra-classe')


PartitionKmeans=Partition(:,nbopt);
[b,listKmeans]=sort(PartitionKmeans,'ascend');
MesFeatureKmeansOrd=MesFeature(listKmeans,listKmeans);

%% M�thodes spectral clustering
MatAff=CreateMatAff(Dataset(:,2:24));
PartitionSC=MethodeSC(MatAff,nbopt);

%% Affichage des r�sultats
[a,listSC]=sort(PartitionSC,'ascend');
MesFeatureSCOrd=MesFeature(listSC,listSC);
MatAffSCord=MatAff(listSC,listSC);
MatAffKmeansord=MatAff(listKmeans,listKmeans);
figure
subplot(1,2,1)
imagesc(MesFeatureKmeansOrd)
hold on 
colorbar
title('Kmeans')
subplot(1,2,2)
imagesc(MesFeatureSCOrd)
colorbar
title('Spectral Clustering')

figure
subplot(1,2,2)
imagesc(MatAffSCord)
hold on 
colorbar
title('Spectral Clustering')
subplot(1,2,1)
imagesc(MatAffKmeansord)
colorbar
title('Kmeans')



% % M�thode hi�rarchique
% MatSim=importdata('Feature_Video.out');
% p=size(MatSim,1);
% A=triu(MatSim,1)+tril(-ones(p));
% list=find(A~=-1);
% Y=linkage(A(list));
% figure
% dendrogram(Y)
% hold on 
% title('Hierarchique')



%% PostTraitement
fichier='ResultatVideo';

Titre=importdata('finalVideoList.txt');

fid=fopen(strcat(fichier,'Kmeans','.txt'),'w');
for i=1:nbopt
    fprintf(fid,'%s\n', strcat('Classe ',num2str(i)));
    ii=find(PartitionKmeans==i);
    for i=1:size(ii,1)
        fprintf(fid,'%s\n', Titre{ii(i)});
    end
    fprintf(fid,'\n\n');
end

fid=fopen(strcat(fichier,'SC','.txt'),'w');
for i=1:nbopt
    fprintf(fid,'%s\n', strcat('Classe ',num2str(i)));
    ii=find(PartitionSC==i);
    for i=1:size(ii,1)
        fprintf(fid,'%s\n', Titre{ii(i)});
    end
    fprintf(fid,'\n\n');
end

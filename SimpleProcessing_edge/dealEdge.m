clear
clc
f = imread('woman.tif');
subplot(2,2,1),imshow(f),title('ԭͼ');
f = rgb2gray(f);  %��ԭͼ�Ĳ�ɫͼת��Ϊ�Ҷ�ͼ��
[M,N] = size(f);
%sobel����
A = [
    -1 -2 -1;
    0 0 0;
    1 2 1
    ];
B = [
    -1 0 1;
    -2 0 2;
    -1 0 1
    ];
%��һ�ֱ�Ե����㷨
J = conv2(double(f),B); 
I = conv2(double(f),A);
K1 = abs(J) + abs(I);
subplot(2,2,2),imshow(K1,[]),title('sobel���ӱ�Ե���ͼ��');
%�ڶ��ֱ�Ե����㷨
HA = imfilter(double(f),A);
HB = imfilter(double(f),B);
K2 = abs(HA) + abs(HB);
subplot(2,2,3),imshow(K2,[]),title('sobel2���ӱ�Ե���ͼ��');
%�����ֱ�Ե����㷨
G = edge(f,'sobel');
subplot(2,2,4),imshow(G,[]),title('matlab�ṩ�ĺ���edge');

%����ͼ���ֵ����ֵ����
y = 100;
for i=1:1:M
    for j = 1:1:N
        if K2(i,j)<y
            K3(i,j) = 0;
        else
            K3(i,j) = 255;
        end
    end
end
figure;
imshow(K3,[]),title('���ͼ���ֵ��');

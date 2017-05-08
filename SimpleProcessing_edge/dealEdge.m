clear
clc
f = imread('woman.tif');
subplot(2,2,1),imshow(f),title('原图');
f = rgb2gray(f);  %将原图的彩色图转化为灰度图像
[M,N] = size(f);
%sobel算子
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
%第一种边缘检测算法
J = conv2(double(f),B); 
I = conv2(double(f),A);
K1 = abs(J) + abs(I);
subplot(2,2,2),imshow(K1,[]),title('sobel算子边缘检测图像');
%第二种边缘检测算法
HA = imfilter(double(f),A);
HB = imfilter(double(f),B);
K2 = abs(HA) + abs(HB);
subplot(2,2,3),imshow(K2,[]),title('sobel2算子边缘检测图像');
%第三种边缘检测算法
G = edge(f,'sobel');
subplot(2,2,4),imshow(G,[]),title('matlab提供的函数edge');

%进行图像二值化二值处理
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
imshow(K3,[]),title('检测图像二值化');

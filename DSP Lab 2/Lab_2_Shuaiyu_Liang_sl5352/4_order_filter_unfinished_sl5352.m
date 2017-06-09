clc;clear all; close all;
%% 
Fs = 8000;
fs = 400;
T = 1;
f = fs/Fs;
w = 2 * pi * f;

%% input time parameters
Tpeak = 0.3;
Tdecay = 0.9;
npeak = Tpeak/T*Fs;
ndecay = Tdecay/T*Fs;
% this part lack of n and r
a11 = -2*r1*cos(w);
a12 = r1^2;
a21 = -2*r1*cos(w);
a22 = r2^2;

a1 = [1,a11,a12];
a2 = [1,a21,a22];
b = 1;

%% Impulse response
imp = [1 zeros(1,N)];
h = filter(b,a1,imp);
h = filter(b,a2,h);
figure(1)
plot(n/Fs,h);
title('Impulse response');
xlabel('Time');

function second_order_recursive_filter_GUI
fc = 1.5;
B = 1;
G = 1;
%%
figure(1);
clf
subplot(321)
b1 = [1 0 -1];
a1 = [2 2*cos(fc) 0];
[H1, om] = freqz(b1, a1);
line_handle1 = line(om/pi, abs(H1));
title( sprintf('Frequency Response. Cut-off frequency = %.3f', fc) )
xlabel('\omega (\pi rad/sample)')
ylim([0 1]);

subplot(322)
zplane(b1,a1);
%%
subplot(323)
b2 = [tan(B/2) 0 -tan(B/2)];
a2 = [tan(B/2)+1 2*cos(0.5*pi) 1-tan(B/2)];
[H2, om] = freqz(b2, a2);
line_handle2 = line(om/pi, abs(H2));
title( sprintf('Frequency Response. Bandwidth = %.3f', B) )
xlabel('\omega (\pi rad/sample)')
ylim([0 1]);

subplot(324)
zplane(b2,a2);
%%
subplot(325)
b3 = [G 0 -G];
a3 = [2 2*cos(0.5*pi) 0];
[H3, om] = freqz(b3, a3);
line_handle3 = line(om/pi, abs(H3));
title( sprintf('Frequency Response. Gain = %.3f', G) )
xlabel('\omega (\pi rad/sample)')
ylim([0 2]);

subplot(326)
zplane(b3,a3);


drawnow;

slider_handle1 = uicontrol('Style', 'slider', ...
    'Min', 0.1, 'Max', pi, ...
    'Value', fc, ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position', [0.12 0.65 0.35 0.01], ...
    'horizontalalignment','left',...
    'Callback',  {@fun1, line_handle1}  );

slider_handle2 = uicontrol('Style', 'slider', ...
    'Min', 0.5, 'Max', pi/2, ...
    'Value', B, ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position',  [0.12 0.35 0.35 0.01], ...
    'horizontalalignment','left',...
    'Callback',  {@fun2, line_handle2}  );

slider_handle3 = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 2, ...
    'Value', G, ...
    'SliderStep', [0.02 0.05], ...
    'units', 'normalized', ...
    'Position',  [0.12 0.05 0.35 0.01], ...
    'horizontalalignment','left',...
    'Callback',  {@fun3,  line_handle3}  );



end


% callback function fun1

function fun1(hObject, eventdata, line_handle1)


fc = get(hObject, 'Value');     % cut-off frequency
fc = max(0.1, fc);             % minimum value
fc = min(pi, fc);             % maximum value

subplot(3,2,1)
b1 = [1 0 -1];
a1 = [2 2*cos(fc) 0];
[H1, om] = freqz(b1, a1);
set(line_handle1, 'ydata', abs(H1));
title( sprintf('Frequency Response. Cut-off frequency = %.3f', fc) )

subplot(3,2,2)
zplane(b1,a1);

end

function fun2(hObject, eventdata,line_handle2)

B = get(hObject, 'Value');     % bandwidth
B = max(0.1, B);             % minimum value
B = min(pi/2, B);             % maximum value


subplot(3,2,3)
b2 = [tan(B/2) 0 -tan(B/2)];
a2 = [tan(B/2)+1 2*cos(0.5*pi) 1-tan(B/2)];
[H2, om] = freqz(b2, a2);
set(line_handle2, 'ydata', abs(H2));
title( sprintf('Frequency Response. Bandwidth = %.3f', B) )

subplot(3,2,4)
zplane(b2,a2);

end

function fun3(hObject, eventdata, line_handle3)

G = get(hObject, 'Value');     % gain
G = max(0, G);             % minimum value
G = min(2, G);             % maximum value


subplot(3,2,5)
b3 = [G 0 -G];
a3 = [2 2*cos(0.5*pi) 0];
[H3, om] = freqz(b3, a3);
set(line_handle3, 'ydata', abs(H3));
title( sprintf('Frequency Response. Gain = %.3f', G) )

subplot(3,2,6)
zplane(b3,a3);

end
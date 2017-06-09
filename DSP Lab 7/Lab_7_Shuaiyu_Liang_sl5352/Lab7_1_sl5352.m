function filter_gui_example_ver1

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + randn(1, N);        % Input signal

fc = 0.1;
[b, a] = butter(2, fc);       
y = filtfilt(b, a, x);
[H, om] = freqz(b, a);

figure(1)
clf
subplot(211);
line_handle1 = plot(n, x);
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3]);

subplot(212);
line_handle2 = plot(abs(H));
title('Initial filter')
xlabel('points');

drawnow;

slider_handle = uicontrol('Style', 'slider', ...
    'Min', 0, 'Max', 1,...
    'Value', 1, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle1, line_handle2, x});

end


function fun1(hObject, eventdata, line_handle1, line_handle2, x)

fc = get(hObject, 'Value');  % fc : cut-off frequency

fc = max(0.01, fc);         % minimum value
fc = min(0.99, fc);         % maximum value

[b, a] = butter(2, fc);     % Order-2 Butterworth filter
y = filtfilt(b, a, x);
[H, om] = freqz(b, a);

subplot(211);
set(line_handle1, 'ydata',  y);        % Update data in figure
title( sprintf('Output of LPF. Cut-off frequency = %.3f', fc), 'fontsize', 12 )


subplot(212);
set(line_handle2, 'ydata', abs(H));
title( sprintf('Transfer Function. Cut-off Frequency = %.3f',fc))
end
clear
close all

%%
[time, displacement] = import_probe_data("C:\Users\Owner\Documents\AbaqusTemp\displacement.csv");

after_contact = time>0.1;
time = time(after_contact);
time = time - time(1);

min_dt = min(diff(time));
time_range = max(time) - min(time);
num_samples = floor(time_range / (1/2 * min_dt));
sample_time = linspace(min(time), max(time), num_samples);
sample_freq = 1 / min(diff(sample_time));

displacement = displacement(after_contact);
displacement = interp1(time, displacement, sample_time);
time = sample_time;

% F = nufft(detrend(displacement),time);
% n = length(time);
% f = (0:n-1)/n;
% figure
% plot(f,abs(F))

F = fft(detrend(displacement));
L = length(time);
P2 = abs(F/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = sample_freq * (0:(L/2))/L;

figure
loglog(f, P1);

%%
[time, velocity] = import_probe_data("C:\Users\Owner\Documents\AbaqusTemp\velocity.csv");

after_contact = time>0.1;
time = time(after_contact);
time = time - time(1);

min_dt = min(diff(time));
time_range = max(time) - min(time);
num_samples = floor(time_range / (1/2 * min_dt));
sample_time = linspace(min(time), max(time), num_samples);
sample_freq = 1 / min(diff(sample_time));

velocity = velocity(after_contact);
velocity = interp1(time, velocity, sample_time);
time = sample_time;

% F = nufft(velocity,time);
% n = length(time);
% f = (0:n-1)/n;
% figure
% plot(f,abs(F))

F = fft(velocity);
L = length(time);
P2 = abs(F/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = sample_freq * (0:(L/2))/L;

figure
loglog(f, P1);

%%
[time, acceleration] = import_probe_data("C:\Users\Owner\Documents\AbaqusTemp\acceleration.csv");

after_contact = time>0.1;
time = time(after_contact);
time = time - time(1);

min_dt = min(diff(time));
time_range = max(time) - min(time);
num_samples = floor(time_range / (1/2 * min_dt));
sample_time = linspace(min(time), max(time), num_samples);
sample_freq = 1 / min(diff(sample_time));

acceleration = acceleration(after_contact);
acceleration = interp1(time, acceleration, sample_time);
time = sample_time;

% F = nufft(acceleration,time);
% n = length(time);
% f = (0:n-1)/n;
% figure
% plot(f,abs(F))

F = fft(acceleration);
L = length(time);
P2 = abs(F/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = sample_freq * (0:(L/2))/L;

figure
loglog(f, P1);

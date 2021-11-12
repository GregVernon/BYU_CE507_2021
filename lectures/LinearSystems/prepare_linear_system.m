function [K, M, f] = prepare_linear_system(K, M, f)
%% Expand size of load vector
if size(f,1) < size(K,2)
    f(end+1 : size(K,2)) = 0;
end
%% Remove boundary conditions
idx = find(max(K) > 1e35);
K(idx,:) = [];
K(:,idx) = [];
M(idx,:) = [];
M(:,idx) = [];
f(idx) = [];
end
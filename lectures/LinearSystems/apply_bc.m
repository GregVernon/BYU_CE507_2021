function [K, f] = apply_bc(K, f)

if size(f, 1) < size(K,2)
    f(end+1:length(K)) = 0;
end

idx = find(max(K) > 1e35);
K(idx,:) = [];
K(:,idx) = [];
f(idx) = [];

end
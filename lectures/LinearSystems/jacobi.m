function [x, resvec] = jacobi(A, b, x0, tol, maxiter)

if isempty(x0)
    x0 = zeros(size(A,1),1);
end

D = diag(diag(A));
L = tril(A,-1);
U = triu(A, 1);

% iD = diag(1./D);
R = L + U;

x = x0;
resvec = zeros(maxiter,1);
for ii = 1:maxiter
    x = D \ ( b - R * x );
    resvec(ii) = norm(A*x - b);
    if resvec(ii) <= tol
        break
    end
end

end
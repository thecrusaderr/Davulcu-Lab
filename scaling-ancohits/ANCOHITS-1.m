function [s1, s2] = ANCOHITS(A, epsilon)

%CoScaling using ANCO-HITS algorithm
maxIter=1000;
s1 = ones(size(A,1),1);

for i=1:maxIter
    s1old = s1;
    s2 = (A' * s1) ./ (abs(A') * abs(s1) + realmin); 
    s1 = (A  * s2) ./ (abs(A)  * abs(s2) + realmin); 
    diff = norm(s1-s1old);
    if(abs(diff)<=epsilon) 
        break 
    end
end
end
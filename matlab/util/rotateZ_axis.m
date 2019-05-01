function R = rotateZ_axis(angle)
% angle: degree of angle
% rotate coordinate X axis
% https://en.wikipedia.org/wiki/Rotation_matrix + transpose
% http://mathworld.wolfram.com/RotationMatrix.html
angle = deg2rad(angle);
s = sin(angle);
c = cos(angle);

R = zeros(3, 3);
R(1,1) = c; R(1, 2) = -s;
R(2,1) = s; R(2, 2) = c;
                        R(3,3) = 1;
R = R';
end
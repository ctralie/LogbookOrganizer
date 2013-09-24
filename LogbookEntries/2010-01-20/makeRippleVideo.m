function [] = makeRippleVideo()
    range = -1:0.01:1;
    [X, Y] = meshgrid(range, range);
    R = sqrt(X.*X + Y.*Y);
    for freqDiv = 1:50;
       Z = cos(R.*freqDiv);
       imwrite(Z, sprintf('ripple%i.png', freqDiv), 'PNG');
    end
    system(sprintf('ffmpeg -f image2 -r 4 -i ripple%s.png -r 4 ripple.ogg', '%d'));
    system('rm ripple*.png');
end
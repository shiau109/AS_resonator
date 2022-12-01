function [I_signal_vs_drm_,Q_signal_vs_drm_] = ro_sig(inputArg1,inputArg2)
global Aad
global Ard
global delta_as
global delta_rm
global chi
global gamma
global gamma_phi
global kappa
global ti_ad
global tf_ad
global ti_rd
global tf_rd

delta_ar = wa-wr;
chi = -(g.^2./delta_ar).*( Ec./(delta_ar-Ec) );

gamma = 0.00019* 2*pi;%[GHz]
gamma_phi = 0 * 2*pi;%[GHz]
kappa = 0.00169 * 2*pi;%[GHz]
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
wad = wa + 3*chi;%[GHz]
wrd_list = wr - chi*linspace(-4,4,100);%[GHz]

I_signal_vs_drm = [];
Q_signal_vs_drm = [];

N_average = 20;
pi_pulse_length = 10; %[ns]
Aad = 0; %pi/pi_pulse_length;

for mm = 1:length(wrd_list)
    wrd = wrd_list(mm);
    delta_as = wa-wad;
    delta_rm = wr-wrd;


    Ard = sqrt(N_average)*0.5*kappa;%[GHz]
    ti_ad = 0;%[ns]
    tf_ad = ti_ad + pi_pulse_length;%[ns]
    ti_rd = tf_ad;%[ns]
    tf_rd = Inf;%Inf[ns]

    tspan = [0 1500];%[ns]
    tq = linspace(tspan(1), tspan(end), 200);
    X0 = 0;
    Y0 = 0;
    Z0 = -1;
    a0 = 0;
    N0 = a0^2;
    aX0 = a0*X0;
    aY0 = a0*Y0;
    aZ0 = a0*Z0;
    y0 = [X0 Y0 Z0 a0 N0 aX0 aY0 aZ0]; %X Y Z a N aX aY aZ
    [t,y] = ode15s(@(t,y) odefcn(t,y), tspan, y0);

    X = y(:,1);
    Y = y(:,2);
    Z = y(:,3);
    a = y(:,4);
    N = y(:,5);
    aX = y(:,6);
    aY = y(:,7);
    aZ = y(:,8);
    I_signal = 1e9*sqrt(Z_TL*h_bar*wr*kappa)*real(a);
    Q_signal = 1e9*sqrt(Z_TL*h_bar*wr*kappa)*imag(a);
    Pe = 0.5*(1+real(Z));
    Pg = 0.5*(1-real(Z));
    
    Iq = interp1(t,I_signal,tq);
    Qq = interp1(t,Q_signal,tq);
    I_signal_vs_drm = [I_signal_vs_drm; Iq];
    Q_signal_vs_drm = [Q_signal_vs_drm; Qq];
end


I_signal_vs_drm_ = I_signal_vs_drm;
Q_signal_vs_drm_ = Q_signal_vs_drm;



end


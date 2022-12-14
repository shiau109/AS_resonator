% clear all
global Aad
global Ard
global delta_as
global delta_rm
global delta_ar
global chi
global gamma
global gamma_phi
global kappa
global ti_ad
global tf_ad
global ti_rd
global tf_rd
h_bar = 1.05457180013e-34;	% 	[J·s]
Z_TL = 50;%[ohm]

wa = 4.0485 * 2*pi;%[GHz]
wr = 6.3687 * 2*pi;%[GHz]
Ec = 0.222 * 2*pi;%[GHz]
g = 0.046 * 2*pi;%[GHz]
% g = 0 * 2*pi;%[GHz]
delta_ar = wa-wr;
chi_01 = (g.^2./delta_ar);
chi = -chi_01*( Ec./(delta_ar-Ec) );
disp( chi );
gamma = 0.0002* 2*pi;%[GHz]
gamma_phi = 0 * 2*pi;%[GHz]
kappa = 0.00006 * 2*pi;%[GHz]

n_c = (delta_ar/g)^2/4
disp( "nc" );
disp( n_c );

disp( "\kappa/(2*\chi)" );
disp( kappa/(2*chi) );

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
wad = wa + 0*chi;%[GHz]

wrd_list = wr +chi*linspace(-10,10,100);%[GHz]
N_average = n_c;
pi_pulse_length = 20;%[ns]
I_signal_vs_drm_g = [];
Q_signal_vs_drm_g = [];
I_signal_vs_drm_e = [];
Q_signal_vs_drm_e = [];
for mm = 1:length(wrd_list)
    wrd = wrd_list(mm);
    delta_as = wa-wad;
    delta_rm = wr-wrd;
    tspan = [0 8000];%[ns]
    tq = linspace(tspan(1), tspan(end), 8000);
    X0 = 0;
    Y0 = 0;
    Z0 = -1;
    a0 = 0;
    N0 = a0^2;
    aX0 = a0*X0;
    aY0 = a0*Y0;
    aZ0 = a0*Z0;
    y0 = [X0 Y0 Z0 a0 N0 aX0 aY0 aZ0]; %X Y Z a N aX aY aZ


    Aad = 0;%pi/pi_pulse_length;%[GHz]   %Rabi freq. = 2*Aad,   2*Aad*pi_pulse_length = pi
    Ard = sqrt(N_average)*0.5*kappa;%[GHz]
    ti_ad = 0;%[ns]
    tf_ad = ti_ad + pi_pulse_length;%[ns]
    ti_rd = tf_ad;%[ns]
    tf_rd = Inf;%Inf[ns]

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
    I_signal_vs_drm_g = [I_signal_vs_drm_g; Iq];
    Q_signal_vs_drm_g = [Q_signal_vs_drm_g; Qq];

    Aad = 0.15708;%pi/pi_pulse_length;%[GHz]   %Rabi freq. = 2*Aad,   2*Aad*pi_pulse_length = pi
 
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
    I_signal_vs_drm_e = [I_signal_vs_drm_e; Iq];
    Q_signal_vs_drm_e = [Q_signal_vs_drm_e; Qq];
end
% Q_signal_vs_drm = -Q_signal_vs_drm;

% rot_angle = 0.5*pi-angle(I_signal_vs_drm(:,end)+1i*Q_signal_vs_drm(:,end));
% rot_matrix = rot_angle*ones(1,size(I_signal_vs_drm,2));
% I_signal_vs_drm_ = I_signal_vs_drm.*cos(rot_matrix)-Q_signal_vs_drm.*sin(rot_matrix);
% Q_signal_vs_drm_ = I_signal_vs_drm.*sin(rot_matrix)+Q_signal_vs_drm.*cos(rot_matrix);


%I_signal_vs_drm_ = I_signal_vs_drm;
%Q_signal_vs_drm_ = Q_signal_vs_drm;

normal_f = (wrd_list-wr)/chi;
[Time,dmr] = meshgrid(tq,normal_f);

% figure(1)
% hold on
% Z_data = 1e3*I_signal_vs_drm_;
% plot(Time,Z_data,'-r')
% Z_data = 1e3*Q_signal_vs_drm_;
% plot(Time,Z_data,'--r')
% xlabel('t (ns)','fontsize',16);
% ylabel('IQ (mV)','fontsize',16);


figure(1)
hold on
Z_data = I_signal_vs_drm_g-I_signal_vs_drm_e;
surf(Time,dmr,Z_data)
shading interp
xlabel('t (ns)','fontsize',16);
ylabel('\delta_m_r (MHz)','fontsize',16);
zlabel('I (mV)','fontsize',16);
title('I');
set(gcf, 'color', 'white');
colorbar
max_cmap = max(max(abs(Z_data)));
b2r_cmap = b2r(-max_cmap,max_cmap);
colormap(b2r_cmap);
box on

figure(2)
hold on
Z_data = Q_signal_vs_drm_g-Q_signal_vs_drm_e;
surf(Time,dmr,Z_data)
shading interp
xlabel('t (ns)','fontsize',16);
ylabel('\delta_m_r (MHz)','fontsize',16);
zlabel('Q (mV)','fontsize',16);
title('Q');
set(gcf, 'color', 'white');
colorbar
max_cmap = max(max(abs(Z_data)));
b2r_cmap = b2r(-max_cmap,max_cmap);
colormap(b2r_cmap);
box on

figure(3)
hold on
Z_data = sqrt(I_signal_vs_drm_g.^2+Q_signal_vs_drm_g.^2)-sqrt(I_signal_vs_drm_e.^2+Q_signal_vs_drm_e.^2);
surf(Time,dmr,Z_data)
shading interp
xlabel('t (ns)','fontsize',16);
ylabel('\delta_m_r (MHz)','fontsize',16);
zlabel('A (mV)','fontsize',16);
title('sqrt(I^2+Q^2)');
set(gcf, 'color', 'white');
colorbar
max_cmap = max(max(abs(Z_data)));
b2r_cmap = b2r(-max_cmap,max_cmap);
colormap(b2r_cmap);
box on


figure(4)
hold on
Z_data = angle(I_signal_vs_drm_g+1i*Q_signal_vs_drm_g)-angle(I_signal_vs_drm_e+1i*Q_signal_vs_drm_e);
surf(Time,dmr,Z_data)
shading interp
xlabel('t (ns)','fontsize',16);
ylabel('\delta_m_r (MHz)','fontsize',16);
zlabel('\phi','fontsize',16);
title('\phi');
set(gcf, 'color', 'white');
colorbar
%max_cmap = max(max(abs(Z_data)));
%b2r_cmap = b2r(-max_cmap,max_cmap);
%colormap(b2r_cmap);
box on

figure(5)
hold on
Z_data = sqrt( (I_signal_vs_drm_g-I_signal_vs_drm_e).^2+ (Q_signal_vs_drm_g-Q_signal_vs_drm_e).^2);
surf(Time,dmr,Z_data)
shading interp
xlabel('t (ns)','fontsize',16);
ylabel('\delta_m_r (MHz)','fontsize',16);
zlabel('A (mV)','fontsize',16);
title('sqrt(dI^2+dQ^2)');
set(gcf, 'color', 'white');
colorbar
max_cmap = max(max(abs(Z_data)));
b2r_cmap = b2r(0,max_cmap);
colormap(b2r_cmap);
box on
disp( "Max S" );

disp( max_cmap );
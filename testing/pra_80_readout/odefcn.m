function dydt = odefcn(t,y)
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
dydt = zeros(8,1);
dydt(4) = -1i*delta_rm*y(4)-1i*chi*y(8)-1i*Ard*(t>ti_rd && t<tf_rd)-0.5*kappa*y(4);
dydt(3) = Aad*(t>ti_ad && t<tf_ad)*y(2)-gamma*(1+y(3));
dydt(1) = -(delta_as+2*chi*(y(5)+0.5))*y(2)-(0.5*gamma+gamma_phi)*y(1);
dydt(2) = (delta_as+2*chi*(y(5)+0.5))*y(1)-(0.5*gamma+gamma_phi)*y(2)-Aad*(t>ti_ad && t<tf_ad)*y(3);
dydt(8) = -1i*delta_rm*y(8)-1i*chi*y(4)+Aad*(t>ti_ad && t<tf_ad)*y(7)-1i*Ard*(t>ti_rd && t<tf_rd)*y(3)-gamma*y(4)-(gamma+0.5*kappa)*y(8);
dydt(6) = -1i*delta_rm*y(6)-(delta_as + 2*chi*(y(5)+1))*y(7)-1i*Ard*(t>ti_rd && t<tf_rd)*y(1)-(0.5*gamma+gamma_phi+0.5*kappa)*y(6);
dydt(7) = -1i*delta_rm*y(7)+(delta_as + 2*chi*(y(5)+1))*y(6)-1i*Ard*(t>ti_rd && t<tf_rd)*y(2)-(0.5*gamma+gamma_phi+0.5*kappa)*y(7)-Aad*(t>ti_ad && t<tf_ad)*y(8);
dydt(5) = -2*Ard*(t>ti_rd && t<tf_rd)*imag(y(4))-kappa*y(5);

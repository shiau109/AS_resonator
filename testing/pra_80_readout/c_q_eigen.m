clear all
%%%%%%%%%%%%%% 基本常數與基本物理量 %%%%%%%%%%%%%%%
h_bar = 1.05457180013e-34;	% 	[J·s]
% h_bar = 6.58211928e-16;% 	[eV·s]
% h_bar = 1.054571726e-27;% 	[erg·s]
en = 2.718281828459;

phi0 = 2.06783375846e-15;%	[Wb = kg·m2.s?2·A?1]
e = 1.602176620898e-19;%[C]
kb = 1.3806485279e-23; %	[J/K]
RQ = 0.5*pi*h_bar/e^2;%[ohm]
r = 0.5772156649; %Euler
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear j
clear i


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
dim_c1 = 6; % photon number = 0~(dim_c1-1)    ppppppppppppp
dim_q1 = 6; % state j = 0~(dim_q1-1)      ppppppppppppp

% f_list = linspace(-0.171,-0.166,501);
% f_list = linspace(-0.3,0.3,501);
f_list = 0;%linspace(-0.3,0.3,501);%


%swap point 3.867
wc1 = 2*pi* 6.347437;%[GHz] q2的zero flux w01
w01_f0_q1 = 2*pi* 4.558;%[GHz] q1的zero flux w01
EC_q1 = 0.205 * 2*pi;%[GHz] q1的EC (ECP = 4EC)     pppppppppppppp


% rscale = 0.67;
% Cqb1 =  rscale*4.59e-15; %[F]
% Cqb2 = rscale*4.58e-15; 
% C12 = (700/2400)*0.125e-15;    %0.13e-15 %{q1,q2靠很接近的值};
% 
% Cq1 = 88.046e-15;
% Cq2 = 88.046e-15;
% Cb = 365.48e-15;
Cr1 = 390.7e-15;
C1 = 88.046e-15;
Cg1 = 3.4249e-15;%4.168e-15;

%%%%%%%%  Junction asymmetry
r1 = (127^2)/(90^2);
d1 = (r1-1)/(r1+1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
j1 = 0:(dim_q1-1);
wp0_q1 = w01_f0_q1+EC_q1;%[GHz] q1的zero flux wp =sqrt(8*EJ0*EC)
EJ0_q1 = wp0_q1^2/(8*EC_q1);%[GHz] q1的zero flux EJ

%%%%%%%%%%%%%%%%%%%%%  create 基本的 operator  %%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% 定義各個Hilbert space的Identity  %%%%%%%%%
Ic1 = eye(dim_c1);
Iq1 = eye(dim_q1);
a1 = diag(sqrt(1:(dim_c1-1)),1);
N1 = diag(0:(dim_c1-1));
sm1 = diag(sqrt(1:(dim_q1-1)),1); %qubit c opertor


%c = diag(sqrt(j(2:end)),1);
%%%%%%%%%%%%%%%%%%%%%  拓展基本的 operator  %%%%%%%%%%%%
a1_  = tensor2(a1, Iq1); % Extended a1
N1_  = tensor2(N1, Iq1); 
sm1_ = tensor2(Ic1, sm1);
I_tot = eye(size(a1_));   dim_tot = length(I_tot); %for tensor5, size()中用c1或q1的extended operator


%%%%%%%%%%%%%% 給定flux bias %%%%%%%%%%%%%
E_vs_rband_cf = []; %band index 為列index, filling factor為 行index
E_of_atom_ground_vs_f = []; 
E_of_pure_ground_vs_f = [];
wj_q1_vs_f = [];% q1的個能級隨filling factor的變化 (ground state energy 調整到0)
Eig_states_vs_f = zeros(dim_tot, dim_tot, length(f_list));
for ff = 1:length(f_list)
    f1 = f_list(ff);
%     EJ_q1 = EJ0_q1*abs(cos(f1*pi)); %[GHz] EJ of q1 at flux filling factor=f1
%     EJ_q2 = EJ0_q2*abs(cos(f2*pi)); %[GHz] EJ of q2 at flux filling factor=f2
%     EJ_b = EJ0_b*abs(cos(fb*pi)); %[GHz] EJ of bus at flux filling factor=fb
    EJ_q1 = EJ0_q1*sqrt(cos(f1*pi).^2 + d1^2*sin(f1*pi).^2); %[GHz] EJ of q1 at flux filling factor=f1
   
    % q1的eigen frequency at flux filling factor=f1
    wj_q1 = -EJ_q1+sqrt(8*EJ_q1*EC_q1)*(j1+0.5)-EC_q1*(6*j1.^2+6*j1+3)/12; %#q1的eigen angular frequency
%     wj_q1 = eigE_CPB(EJ_q1, EC_q1,dim_q1).';
    wj_q1 = wj_q1-wj_q1(1);  %Noramlied so that the ground state energy is 0
    w01_q1 = wj_q1(2)-wj_q1(1);  % w01 of q1 at f1
    wj_q1_vs_f = [wj_q1_vs_f wj_q1.'];%不同j(列) 不同f(行)
    
    g01_q1c1 = 0.5*Cg1/sqrt((C1)*(Cr1))*sqrt(w01_q1.*wc1); 
    chi_e_g = -g01_q1c1^2/(w01_q1-wc1)*EC_q1/(w01_q1-wc1-EC_q1);
    chi_e_g_over_2pi = chi_e_g/2/pi;
    %%%%%%%%%%%% wj , epj, 及 g(gij的矩陣) %%%%%%%%%%%%%%%
    %     %%%%%%%%%%    第一階段計算 eigen energy and gij of the qubit
    %     [Em, g] = EigE_gij_of_qubit_k0(EJ,ECP,N_basis_atom);
    %     E_of_atom_ground_vs_f = [E_of_atom_ground_vs_f Em(1)];
    %     Em_list = [Em_list Em]; %band index 為列index, filling factor為 行index
    %     dEm_list = [dEm_list Em(2:end)-Em(1:end-1)]; %dE index 為列index, filling factor為 行index
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%  qubit operator %%%%%%%%%%%%%%%%%%
    Hq1 = diag(wj_q1); 
    
    %%%%%%%%%%%%%%%%%%%%%  create H 的各部分  %%%%%%%%%%%%%%%%%%%%%%%%%%%
    Hc1_ = wc1*N1_;
    Hq1_ = tensor2(Ic1,Hq1); %Extended Hq1 in in the whole H-space
%     H_q1c1_ = g01_q1c1*(a1_'+a1_)*(sm1_+sm1_');
    H_q1c1_ = g01_q1c1*(a1_'*sm1_+a1_*sm1_');
  
 
    
    H = Hc1_+Hq1_+H_q1c1_;
    [eig_vec,eig_val] = eig(H);
%     [eig_vec,eig_val] = eigs(H_sparse);



    E = real(diag(eig_val));
    [E_sorted, IX] = sort(E,'ascend');
    Eig_states = eig_vec(:,IX); % cavity + atom + HI 的eigen states  [vector1 vector2 vector3 ...]
    Eig_states_vs_f(:,:,ff) = Eig_states;
    E_sorted = E_sorted/2/pi; %角頻轉成頻率
    E_of_pure_ground_vs_f = [E_of_pure_ground_vs_f E_sorted(1)];
    E_vs_rband_cf = [E_vs_rband_cf E_sorted]; %band index 為列index, filling factor為 行index
end

fr_state_0g = wj_q1_vs_f(1,:)/2/pi;
fr_state_1g = ( wc1+wj_q1_vs_f(1,:) )/2/pi;

fr_state_0e = wj_q1_vs_f(2,:)/2/pi;
fr_state_1e = ( wc1+wj_q1_vs_f(2,:) )/2/pi;

fr_state_0f = wj_q1_vs_f(3,:)/2/pi;
fr_state_1f = ( wc1+wj_q1_vs_f(3,:) )/2/pi;


r0 = E_vs_rband_cf(3)-E_vs_rband_cf(1)

r1 = E_vs_rband_cf(5)-E_vs_rband_cf(2)

r2 = E_vs_rband_cf(8)-E_vs_rband_cf(4)

(r1-r0)*1e6
(r2-r1)*1e6

% fr_state_10 = wj_q1_vs_f(2,:)/2/pi;
% fr_state_01 = wj_q2_vs_f(2,:)/2/pi;
% fr_state_11 = (wj_q1_vs_f(2,:)+wj_q2_vs_f(2,:))/2/pi;
% fr_state_20 = wj_q1_vs_f(3,:)/2/pi;
% fr_state_02 = wj_q2_vs_f(3,:)/2/pi;
% 
% fr_state_110 = (wj_q1_vs_f(2,:)+wj_b_vs_f(2,:))/2/pi;
% fr_state_011 = (wj_q2_vs_f(2,:)+wj_b_vs_f(2,:))/2/pi;
% fr_state_020 = wj_b_vs_f(3,:)/2/pi;
% fr_state_h20 = 0.5*wj_q1_vs_f(3,:)/2/pi;
% fr_state_h40 = 0.5*wj_q1_vs_f(5,:)/2/pi;











figure(2)
hold on
for pp = 1:12%dim_tot
    eval(['plot(f_list, E_vs_rband_cf(' num2str(pp) ',:)-E_of_pure_ground_vs_f)']);
end
plot(f_list, fr_state_0g,'--b')
plot(f_list, fr_state_1g,'--b')
plot(f_list, fr_state_0e,'--r')
plot(f_list, fr_state_1e,'--r')
plot(f_list, fr_state_0f,'--k')
plot(f_list, fr_state_1f,'--k')
xlabel('Filling factor','fontsize',16);
ylabel('\omega_e_i_g (GHz)','fontsize',16);
set(gcf, 'color', 'white');
box on









% %%%%%   given an f1, search the band index for a given basis state 
% % dim_c1 = 4; % photon number = 0~(dim_c1-1)    ppppppppppppp
% % dim_c2 = 3; % photon number = 0~(dim_c2-1)
% % dim_b = 3; % photon number = 0~(dim_b-1)
% % dim_q1 = 4; % state j = 0~(dim_q1-1)      ppppppppppppp
% % dim_q2 = 3; % state j = 0~(dim_q2-1)
% %%%%%%%%%%%%%%%%%%%%%%%%%%
% state_c1_0 = zeros(dim_c1,1); state_c1_0(1,1) = 1;
% for kk = 1:dim_c1-1
%     eval(['state_c1_' int2str(kk) '= circshift(state_c1_' int2str(kk-1) ',1);']);
% end
% 
% state_c2_0 = zeros(dim_c2,1); state_c2_0(1,1) = 1;
% for kk = 1:dim_c2-1
%     eval(['state_c2_' int2str(kk) '= circshift(state_c2_' int2str(kk-1) ',1);']);
% end
% 
% state_b_0 = zeros(dim_b,1); state_b_0(1,1) = 1;
% for kk = 1:dim_b-1
%     eval(['state_b_' int2str(kk) '= circshift(state_b_' int2str(kk-1) ',1);']);
% end
% 
% state_q1_0 = zeros(dim_q1,1); state_q1_0(1,1) = 1;
% for kk = 1:dim_q1-1
%     eval(['state_q1_' int2str(kk) '= circshift(state_q1_' int2str(kk-1) ',1);']);
% end
% 
% state_q2_0 = zeros(dim_q2,1); state_q2_0(1,1) = 1;
% for kk = 1:dim_q2-1
%     eval(['state_q2_' int2str(kk) '= circshift(state_q2_' int2str(kk-1) ',1);']);
% end
% 
% 
% state_to_search = tensor5(state_c1_1, state_q1_0, state_b_0, state_q2_0, state_c2_0);
% f1_to_study = 0.1; 
% df = f_list(2)-f_list(1);
% idx_f1_to_study = find(abs(f_list-f1_to_study)<=df);
% 
% overlap_vs_band = [];
% for bb = 1:dim_tot %% bb is band index
%     state_to_check = Eig_states_vs_f(:,bb,idx_f1_to_study(1));
%     state_overlap = abs(dot(conj(state_to_check), state_to_search));
%     overlap_vs_band = [overlap_vs_band state_overlap];
% end
% [Max_overlap,Ind_band] = max(overlap_vs_band);
% Ind_band
% 
% 
% 
% 
% 
% 
% 
% % %%% Plot eigen states diagram
% % n_eig = 1;% 看第 n_eig 個 eigenstate
% % if(length(f_list) == 1)
% %     Eig_state_to_plot = reshape(Eig_states(:,n_eig), dim_q, dim_p); %qubit的索引在先, photon的索引在後
% %     %%%%%%%%%%% 畫柱狀圖 %%%%%%
% %     Z = abs(Eig_state_to_plot);
% %     figure(4)
% %     h = bar3(Z);
% %     colormap Cool
% %     colorbar
% %     %Tell handle graphics to use interpolated rather than flat shading
% %     shading interp
% %     % For each barseries, map its CData to its ZData
% %     for i = 1:length(h)
% %         zdata = get(h(i),'ZData');
% %         set(h(i),'CData',zdata)
% %         % Add back edge color removed by interpolating shading
% %         set(h,'EdgeColor','k') 
% %     end
% %     
% %     %%% create YTickLabel
% %     Y_Tick_Label = {'g'};
% %     for jj = 1:dim_q-1
% %         Y_Tick_Label = [Y_Tick_Label, {['e' num2str(jj)]} ];
% %     end
% %     %%%
% %     set(gca,'XTickLabel',m)
% %     set(gca,'YTickLabel',Y_Tick_Label)
% %     xlabel('Photon number','fontsize',12);
% %     ylabel('Qubit eigenstate','fontsize',12);
% %     zlabel('|c_j_m|')
% %     zlim([0 1])
% %     set(gcf, 'color', 'white');
% %     % box on
% % end
% % 
% % 
% % 
% % 
% % %%%  For searching for possible multiphoton transition (只針對算一個f的情況)
% % if(length(f_list) == 1)
% %     Weigij_I = E_vs_rband_cf*ones(1,length(E_vs_rband_cf))-ones(length(E_vs_rband_cf),1)*E_vs_rband_cf.';
% %     Weigij_II = Weigij_I/2;
% %     Weigij_III = Weigij_I/3;
% %     Weigij_IV = Weigij_I/4;
% % end
% 
% 
% 
% % %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %  %%%%   nn(i,j) is normalized n(i,j), where n(i,j)=<i|n|j>. g(i,j)=beta*n(i,j)
% % n(j,j+1) = sqrt(0.5*(j(1:end-1)+1))*(EJ/8/EC)^0.25; (j starts from 0 to dim_q-2)
% %  gij is proportional to nnij, i.e. gij = g01*nnij
% % nn_jp1_j = sqrt(0.5*(j(1:end-1)+1)); %n(j+1,j), j starts from 0 to dim_q-2
% % nn = (diag(nn_jp1_j,1)+diag(nn_jp1_j,-1))/nn_jp1_j(1); %nij matrix. (gij正比於nij)
% % c operator 高到低的所有運作的總和
% % c = zeros(dim_q); %高到低的所有運作
% % for ii =0:(dim_q-2) %(dim_q-1)是上限
% %     for jj = (ii+1):(dim_q-1)
% %         vi = I_q(:,ii+1);
% %         vj = I_q(:,jj+1);
% %         sij = vi*vj';
% %         c = c + nn(ii+1, jj+1)*sij;
% %     end
% % end

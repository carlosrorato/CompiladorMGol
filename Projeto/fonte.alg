inicio
  varinicio
    A lit;
    B inteiro;
    D inteiro;
    C real;
  varfim;
  escreva "Digite B";
  leia B;
  escreva "Digite A:";
  leia A;
  se(B>2)
    entao
    se(B<=4)
      entao
      escreva "B esta entre 2 e 4";
    fimse
  fimse
  B<-B+1;
  B<-B+2;
  B<-B+3;
  D<-B;
  C<-5.0;
  escreva "\nB=\n";
  escreva D;
  escreva "\n";
  escreva C;
  escreva "\n";
  escreva A;
  enquanto (B >= 0) faca
     escreva "iteracao...iterando...";
     B <- B - 1;
     se (B > 5)
     entao
       escreva "Numero maior que cinco";
       D <- 2;
       enquanto (D >= 0) faca
        escreva "imprimindo teste...";
        D <- D - 1;
       fimenquanto
     fimse
   fimenquanto

fim
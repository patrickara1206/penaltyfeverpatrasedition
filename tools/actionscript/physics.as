if(dey >= 0)
{
   lopta.gotoAndStop(14 - lopta._y % 13);
}
brojacSuta++;
xRukavica = golmance._x + golmance.ruk._x * golmance._xscale / 100;
yRukavica = golmance._y + golmance.ruk._y * golmance._yscale / 100;
if(golLinija - senka._y >= 2 * dey and senka._y > golLinija and !gol and !hitLopta)
{
   if(golLinija - senka._y < dey)
   {
      uRuci = golmance.ruk.hitTest(lopta._x,lopta._y,true);
      if(!uRuci)
      {
         x1Lopta = lopta._x + rLopta * 1;
         y1Lopta = lopta._y + rLopta * 0;
         x2Lopta = lopta._x + rLopta * 0.7071;
         y2Lopta = lopta._y + rLopta * 0.7071;
         x3Lopta = lopta._x + rLopta * 0;
         y3Lopta = lopta._y + rLopta * 1;
         x4Lopta = lopta._x + rLopta * -0.7071;
         y4Lopta = lopta._y + rLopta * 0.7071;
         x5Lopta = lopta._x + rLopta * -1;
         y5Lopta = lopta._y + rLopta * 0;
         x6Lopta = lopta._x + rLopta * -0.7071;
         y6Lopta = lopta._y + rLopta * -0.7071;
         x7Lopta = lopta._x + rLopta * 0;
         y7Lopta = lopta._y + rLopta * -1;
         x8Lopta = lopta._x + rLopta * 0.7071;
         y8Lopta = lopta._y + rLopta * -0.7071;
         hit0Lopta = golmance.hitTest(lopta._x,lopta._y,true);
         hit1Lopta = golmance.hitTest(x1Lopta,y1Lopta,true);
         hit2Lopta = golmance.hitTest(x2Lopta,y2Lopta,true);
         hit3Lopta = golmance.hitTest(x3Lopta,y3Lopta,true);
         hit4Lopta = golmance.hitTest(x4Lopta,y4Lopta,true);
         hit5Lopta = golmance.hitTest(x5Lopta,y5Lopta,true);
         hit6Lopta = golmance.hitTest(x6Lopta,y6Lopta,true);
         hit7Lopta = golmance.hitTest(x7Lopta,y7Lopta,true);
         hit8Lopta = golmance.hitTest(x8Lopta,y8Lopta,true);
         hit5 = hit0Lopta + hit1Lopta + hit2Lopta + hit3Lopta + hit4Lopta + hit5Lopta + hit6Lopta + hit7Lopta + hit8Lopta;
         hitLopta = hit5 > 0;
         if(hitLopta)
         {
            zvukPromasaj.start();
            x5 = hit0Lopta * lopta._x + hit1Lopta * x1Lopta + hit2Lopta * x2Lopta + hit3Lopta * x3Lopta + hit4Lopta * x4Lopta;
            x5 += hit5Lopta * x5Lopta + hit6Lopta * x6Lopta + hit7Lopta * x7Lopta + hit8Lopta * x8Lopta;
            x5 /= hit5;
            y5 = hit0Lopta * lopta._y + hit1Lopta * y1Lopta + hit2Lopta * y2Lopta + hit3Lopta * y3Lopta + hit4Lopta * y4Lopta;
            y5 += hit5Lopta * y5Lopta + hit6Lopta * y6Lopta + hit7Lopta * y7Lopta + hit8Lopta * y8Lopta;
            y5 /= hit5;
            rLopta *= 1.01;
            dx = lopta._x - x5;
            if(Math.abs(sabirak) < rLopta)
            {
               y5 = lopta._y;
            }
            dz = lopta._y - y5;
            dx *= 2 * Math.abs(dey) / rLopta;
            dz *= 2 * Math.abs(dey) / rLopta;
            dHitLopta = Math.sqrt(dx * dx + dz * dz);
            rLopta = Math.abs(dey) * 2;
            dy = (1 - dHitLopta / rLopta) * rLopta;
            rezBrzina = Math.sqrt(dex * dex + dey * dey);
            dex = dex / 2 + dx;
            dey += dy;
            dex *= 0.7;
            dey *= 0.7;
            pocbrzina = Math.sqrt(dex * dex + dey * dey);
            rezVisina = maksvisina;
            maksvisina *= Math.abs(rezBrzina / pocbrzina);
            if(maksvisina > 2 * visinaGola)
            {
               maksvisina = 2 * visinaGola;
            }
            rezUgao = Math.asin(Math.abs(sabirak) / maksvisina) - pocetni_ugao;
            omega *= 0.7 + Math.abs(rezVisina / maksvisina) * 0.3;
            if(dz > 0)
            {
               brojac = (3.141592653589793 - rezUgao) / omega;
            }
            else
            {
               brojac = rezUgao / omega;
            }
            pocbrzina = Math.sqrt(dex * dex + dey * dey);
            ugaokretanjarad = 3.141592653589793 - Math.asin(dex / pocbrzina);
         }
         hitLopta = true;
      }
      else
      {
         dex = 0;
         dey = 0;
         lopta.stop();
         senka._visible = false;
      }
   }
}
if(golLinija - senka._y >= dey and senka._y > golLinija and !gol)
{
   brojac = brojac - faktorbrojaca + (golLinija - senka._y) / dey;
   xSenka += (golLinija - ySenka) / dey * dex;
   senka._x += (golLinija - senka._y) / dey * dex;
   ySenka = golLinija;
   senka._y = golLinija;
}
else
{
   xSenka += dex;
   ySenka += dey;
   senka._x += dex;
   senka._y += dey;
}
frameGolman += dFrame;
golmance.gotoAndStop(Math.round(frameGolman));
izgled_igraca();
dxGolman += dexGolman;
dyGolman += deyGolman;
golmance._x = dxGolman;
golmance._y = dyGolman;
if(Math.abs(omega * brojac - 3.141592653589793) < 0.1)
{
   brojac = 0;
   maksvisina *= 0.3;
   omega *= 1.5;
   pocetni_ugao = 0;
   dex *= 0.8;
   dey *= 0.8;
}
brojac += faktorbrojaca;
sabirak = (- maksvisina) * Math.sin(omega * brojac + pocetni_ugao);
lopta._x = !uRuci * senka._x + uRuci * xRukavica;
lopta._y = !uRuci * (senka._y - Math.abs(sabirak)) + uRuci * yRukavica;
dLoptaOsaGola = Math.abs(osaGola - lopta._x);
if(senka._y == golLinija and !gol and !uRuci and dey < 0)
{
   if(lopta._y - lopta._height / 2 >= golLinija - visinaGola and lopta._y <= golLinija)
   {
      if(dLoptaOsaGola < sirinaGola / 2 - lopta._width / 2)
      {
         gol = true;
         uGolu = true;
         golmance.swapDepths(lopta);
         gol_senka.swapDepths(lopta);
         okvirGola.swapDepths(lopta);
         mrezaGornja.swapDepths(lopta);
         zvukGol.setVolume(100);
         zvukGol.start();
      }
      else if(dLoptaOsaGola < sirinaGola / 2 + fiGola + lopta._width / 2)
      {
         zvukStativa.start();
         pr = sirinaGola / 2 + fiGola + lopta._width / 2 - dLoptaOsaGola;
         if(senka._x > osaGola)
         {
            ugaokretanjarad -= pr / (fiGola + lopta._width + 4) * 6.283185307179586;
         }
         else
         {
            ugaokretanjarad += pr / (fiGola + lopta._width + 4) * 6.283185307179586;
         }
         dex = pocbrzina * Math.sin(ugaokretanjarad);
         dey = pocbrzina * Math.cos(ugaokretanjarad);
         if(dey < 0 and !uRuci and Math.abs(osaGola - lopta._x) + lopta._width / 2 < sirinaGola / 2 and lopta._y - lopta._height / 2 >= golLinija - visinaGola and lopta._y <= golLinija)
         {
            zvukGol.start();
            gol = true;
            uGolu = true;
            golmance.swapDepths(lopta);
            gol_senka.swapDepths(lopta);
            okvirGola.swapDepths(lopta);
            mrezaGornja.swapDepths(lopta);
         }
         else
         {
            zvukPromasaj.start();
         }
      }
      else
      {
         zvukPromasaj.start();
      }
   }
   else if(Math.abs(sabirak) < visinaGola + fiGola + lopta._height / 2 and dLoptaOsaGola < sirinaGola / 2 + fiGola / 2)
   {
      zvukStativa.start();
      pr = visinaGola + fiGola + lopta._height / 2 - Math.abs(sabirak);
      rezBrzina = pocbrzina;
      pocbrzina = Math.cos(6.283185307179586 * (pr / (fiGola + lopta._height))) * pocbrzina;
      dex = pocbrzina * Math.sin(ugaokretanjarad);
      dey = pocbrzina * Math.cos(ugaokretanjarad);
      if(dey > 0)
      {
         dex = - dex;
      }
      maksvisina *= Math.abs(rezBrzina / pocbrzina);
      if(maksvisina > 3 * visinaGola)
      {
         maksvisina = 3 * visinaGola;
      }
      rezUgao = Math.asin(Math.abs(sabirak) / maksvisina) - pocetni_ugao;
      omega *= 0.5 + Math.abs(pocbrzina / rezBrzina / 2);
      if(pr / (fiGola + lopta._height) > 0.5)
      {
         brojac = (3.141592653589793 - rezUgao) / omega;
      }
      else
      {
         brojac = rezUgao / omega;
      }
      if(pocbrzina > 0)
      {
         golmance.swapDepths(lopta);
         gol_senka.swapDepths(lopta);
         okvirGola.swapDepths(lopta);
         mrezaGornja.swapDepths(lopta);
         if(brojac * omega > 1.5707963267948966)
         {
            zvukGol.start();
            gol = true;
            uGolu = true;
         }
         else
         {
            zvukPromasaj.start();
         }
      }
      else
      {
         zvukPromasaj.start();
      }
   }
   else
   {
      golmance.swapDepths(lopta);
      gol_senka.swapDepths(lopta);
      okvirGola.swapDepths(lopta);
      mrezaGornja.swapDepths(lopta);
      mrezaGlavna.swapDepths(lopta);
      zvukPromasaj.start();
   }
}
if(gol)
{
   if(Math.abs(sabirak) > visinaGola)
   {
      maksvisina = Math.abs(sabirak);
      brojac = 2.199114857512855 / omega;
      pocetni_ugao = 0;
   }
   if(senka._y <= golLinija - dubinaGola)
   {
      senka._y = golLinija - dubinaGola + 1;
      dex *= 0.05;
      dey *= -0.02;
      maksvisina = Math.abs(sabirak);
      brojac = 1.5707963267948966 / omega;
      pocetni_ugao = 0;
      mrezaGlavna.mreza.gotoAndPlay(2);
   }
   if(dLoptaOsaGola > sirinaGola / 2 - lopta._width / 2 and senka._y < golLinija and uGolu)
   {
      dex *= -0.1;
      dey *= 0.8;
      uGolu = false;
   }
}
if(senka._y < golLinija - 55)
{
   if(lopta._y > golLinija - 100)
   {
      dex *= 0.5;
      dey = (- dey) * 0.5;
   }
   else
   {
      dex = 0;
      dey = 0;
   }
}
if(brojacSuta > trajanjeSuta)
{
   strelica.removeMovieClip();
   strelica2.removeMovieClip();
   senka.removeMovieClip();
   lopta.removeMovieClip();
   igr.removeMovieClip();
   golmance.removeMovieClip();
   meta.removeMovieClip();
   meta2.removeMovieClip();
   Mouse.removeListener(mouseListener1);
   zvukShut.setVolume(100);
   igr_golovi += sutIgraca * gol;
   komp_golovi += !sutIgraca * gol;
   if(sutIgraca)
   {
      gotoAndStop("provera_kraja_1");
      play();
   }
   else
   {
      gotoAndStop("provera_kraja_2");
      play();
   }
}


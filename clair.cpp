#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main(int argc, char **argv)
{
   string texteChiffre;
   string texteClaire;
   int longueurTexteChiffre;
   int longueurTexteClaire;
   int difference;
   char lettre1, lettre2,clef;

   cout << "Entrez le texte chiffre en majuscule sans caractere accentue : ";
   getline(cin,texteChiffre);

   cout << "Entrez le texte clair en majuscule sans caractere accentue : ";
   getline(cin,texteClaire);
   
   
   longueurTexteChiffre = texteChiffre.length();
   longueurTexteClaire = texteClaire.length();

   if(longueurTexteClaire > longueurTexteChiffre)
   {
      cout << "La longueur du texte clair doit etre inferieur ou egale a la longueur du texte chiffre" << endl;
      return 0;
   }

   cout << "Resultat de la clef" << endl;
   
   for(int i=0; i < longueurTexteClaire; i++)
   {
      lettre1 = texteChiffre.at(i) - 'A';
      lettre2 = texteClaire.at(i) - 'A';

      difference = (lettre1 - lettre2);

      if(difference < 0)
      {
         clef = char(65+(26 - abs(difference)));
      }
      else
      {
         clef = char(difference + 65); 
      }
      cout << clef;
   }

   cout << endl;

   return 0;
}
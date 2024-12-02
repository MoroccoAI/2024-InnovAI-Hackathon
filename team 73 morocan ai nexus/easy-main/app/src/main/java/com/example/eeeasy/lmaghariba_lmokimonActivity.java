
package com.example.eeeasy;

import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

public class lmaghariba_lmokimonActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lmaghariba_lmokimon);

        // Configurer le Toolbar
        Toolbar toolbar = findViewById(R.id.toolbar);  // Assurez-vous d'avoir un Toolbar dans votre layout
        setSupportActionBar(toolbar);
    }

    // Inflater le menu
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Gonfler le menu depuis le fichier XML
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    // Gérer les sélections du menu
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        // Vérifier quel item du menu a été sélectionné
        if (id == R.id.nav_home) {
            // Logique pour l'élément "Home"
            // Ajoutez ici l'action que vous souhaitez pour cet élément
            return true;
        } else if (id == R.id.nav_Khadamat_mouatine) {
            // Logique pour l'élément "Khadamat Mouatine"
            // Ajoutez ici l'action que vous souhaitez pour cet élément
            return true;
        } else if (id == R.id.nav_help) {
            // Logique pour l'élément "Help"
            // Ajoutez ici l'action que vous souhaitez pour cet élément
            return true;
        } else if (id == R.id.nav_profile) {
            // Logique pour l'élément "Profile"
            // Ajoutez ici l'action que vous souhaitez pour cet élément
            return true;
        } else if (id == R.id.nav_logout) {
            // Logique pour l'élément "Logout"
            // Ajoutez ici l'action que vous souhaitez pour cet élément
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}

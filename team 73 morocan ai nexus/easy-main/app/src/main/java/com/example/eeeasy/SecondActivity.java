package com.example.eeeasy;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.material.navigation.NavigationView;

public class SecondActivity extends AppCompatActivity {

    private DrawerLayout drawerLayout;
    private NavigationView navigationView;
    private Toolbar toolbar;
    private ImageButton ikonAjanib, ikonSoya, ikonLmaghariba, ikonMagharibabilkharij;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);

        // Initialisation des composants
        drawerLayout = findViewById(R.id.main);
        navigationView = findViewById(R.id.nav_view);
        toolbar = findViewById(R.id.toolbar);
        ikonAjanib = findViewById(R.id.ikon_ajanib);
        ikonSoya = findViewById(R.id.ikon_soyah);
        ikonLmaghariba = findViewById(R.id.ikon_lmaghariba);
        ikonMagharibabilkharij = findViewById(R.id.ikon_magharibabilkharij);

        // Configurer la Toolbar
        setSupportActionBar(toolbar);

        // Configurer le DrawerLayout avec la Toolbar
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawerLayout, toolbar,
                R.string.navigation_drawer_open,
                R.string.navigation_drawer_close
        );
        drawerLayout.addDrawerListener(toggle);
        toggle.syncState();

        // Apporte la vue de navigation devant
        navigationView.bringToFront();

        // Gérer les actions des boutons
        ikonAjanib.setOnClickListener(v -> {
            // Action pour le bouton "الاجانب المقيمون بالمغرب"
            Intent intent = new Intent(SecondActivity.this, ajanib_mo9imounActivity.class);
            startActivity(intent);
        });

        ikonSoya.setOnClickListener(v -> {
            // Action pour le bouton "السياح الاجانب"
            Intent intent = new Intent(SecondActivity.this, soyah_ajanibActivity.class);
            startActivity(intent);
        });

        ikonLmaghariba.setOnClickListener(v -> {
            // Action pour le bouton "المغارب المقيمون"
            Intent intent = new Intent(SecondActivity.this, lmaghariba_lmokimonActivity.class);
            startActivity(intent);
        });

        ikonMagharibabilkharij.setOnClickListener(v -> {
            // Action pour le bouton "المغارب بالخارج"
            Intent intent = new Intent(SecondActivity.this, maghariba_bilkharijActivity.class);
            startActivity(intent);
        });
    }

    @Override
    public void onBackPressed() {
        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public void onResume() {
        super.onResume();
        drawerLayout.setDrawerLockMode(DrawerLayout.LOCK_MODE_UNLOCKED);
    }
}

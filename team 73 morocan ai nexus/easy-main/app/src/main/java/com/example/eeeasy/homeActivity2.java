package com.example.eeeasy;

import android.content.Intent;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.View;
import android.widget.ImageButton;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.drawerlayout.widget.DrawerLayout;
import com.google.android.material.navigation.NavigationView;
import android.animation.ValueAnimator;
import android.view.animation.LinearInterpolator;
import androidx.core.view.GravityCompat;


public class homeActivity2 extends AppCompatActivity {
    private DrawerLayout drawerLayout;
    private NavigationView navigationView;
    private Toolbar toolbar;
    private ImageButton logoCenter, logoTop, logoBottom, logoLeft, logoRight;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home2);

        // Initialisation des composants
        drawerLayout = findViewById(R.id.main);
        navigationView = findViewById(R.id.nav_view);
        toolbar = findViewById(R.id.toolbar);
        logoCenter = findViewById(R.id.ikon_soyah);
        logoTop = findViewById(R.id.logo_top);
        logoBottom = findViewById(R.id.logo_bottom);
        logoLeft = findViewById(R.id.logo_left);
        logoRight = findViewById(R.id.logo_right);

        // Configuration de la Toolbar
        setSupportActionBar(toolbar);

        // Configuration du DrawerLayout avec la Toolbar
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawerLayout, toolbar,
                R.string.navigation_drawer_open,
                R.string.navigation_drawer_close
        );
        drawerLayout.addDrawerListener(toggle);
        toggle.syncState();
        navigationView.bringToFront();

        // Action pour le logo du haut
        logoTop.setOnClickListener(v -> {
            Intent intent = new Intent(homeActivity2.this, SecondActivity.class);
            startActivity(intent);
        });

        // Démarrer l'animation circulaire
        animateButtons(3000, 80);  // Durée de 3 secondes, rayon de 80dp
    }

    private void animateButtons(int duration, float radius) {
        ValueAnimator animator = ValueAnimator.ofFloat(0, 360);
        animator.setDuration(duration);
        animator.setInterpolator(new LinearInterpolator());
        animator.addUpdateListener(animation -> {
            float angle = (float) animation.getAnimatedValue();

            // Convertir le rayon de dp à pixels
            float radiusPx = TypedValue.applyDimension(
                    TypedValue.COMPLEX_UNIT_DIP,
                    radius,
                    getResources().getDisplayMetrics()
            );

            // Mettre à jour les positions des boutons pour effectuer une rotation en cercle
            updateButtonPosition(logoTop, radiusPx, angle, 0);
            updateButtonPosition(logoRight, radiusPx, angle, 90);
            updateButtonPosition(logoBottom, radiusPx, angle, 180);
            updateButtonPosition(logoLeft, radiusPx, angle, 270);
        });

        // Démarrer l'animation une seule fois
        animator.start();
    }

    private void updateButtonPosition(View button, float radius, float angle, float offset) {
        // Calculer la position en fonction de l'angle
        double radians = Math.toRadians(angle + offset);
        float x = (float) (radius * Math.cos(radians));
        float y = (float) (radius * Math.sin(radians));

        // Appliquer les nouvelles positions pour déplacer les boutons
        button.setTranslationX(x);
        button.setTranslationY(y);
    }

    @Override
    public void onBackPressed() {
        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }
}

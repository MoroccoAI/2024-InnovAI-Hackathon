package com.example.eeeasy;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.TranslateAnimation;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private static final int SPLASH_TIMER = 3000; // Durée d'affichage du splash (3 secondes)

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Charger votre fichier XML

        // Trouver les éléments de la mise en page
        ImageView rectongleb = findViewById(R.id.imageView);
        ImageView rectangle = findViewById(R.id.imageView3);
        ImageView eeasy = findViewById(R.id.imageView4);

        // Appliquer des animations de flottement
        applyFloatingAnimation(rectongleb);
        applyFloatingAnimation(rectangle);
        applyFloatingAnimation(eeasy);

        // Naviguer vers l'activité principale après le délai
        new Handler().postDelayed(() -> {
            Intent intent = new Intent(MainActivity.this, homeActivity.class);
            startActivity(intent);
            finish(); // Fermer l'activité Splash
        }, SPLASH_TIMER);
    }

    // Méthode pour appliquer une animation de flottement à une ImageView
    private void applyFloatingAnimation(ImageView imageView) {
        Animation floatAnimation = new TranslateAnimation(0, 0, -20, 20); // Mouvement vertical (haut en bas)
        floatAnimation.setDuration(1500); // Durée de l'animation (1.5 secondes)
        floatAnimation.setRepeatMode(Animation.REVERSE); // Revenir à l'état initial
        floatAnimation.setRepeatCount(Animation.INFINITE); // Animation infinie
        imageView.startAnimation(floatAnimation);
    }
}

package com.example.eeeasy;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class homeActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        // Charger les animations
        Animation fadeIn = AnimationUtils.loadAnimation(this, R.anim.fade_in);
        Animation slideIn = AnimationUtils.loadAnimation(this, R.anim.slide_in);
        Animation zoomIn = AnimationUtils.loadAnimation(this, R.anim.zoom_in);

        // Lier les vues
        ImageView logoImageView = findViewById(R.id.logoImageView);
        TextView welcomeTextView = findViewById(R.id.welcomeTextView);
        TextView descriptionTextView = findViewById(R.id.descriptionTextView);
        Button btnLogin = findViewById(R.id.btnLogin);
        Button btnRegister = findViewById(R.id.btnRegister);

        // Appliquer l'animation de glissement et de zoom à l'image du logo
        logoImageView.startAnimation(zoomIn);

        // Appliquer l'animation de fondu sur le texte et les boutons
        welcomeTextView.startAnimation(fadeIn);
        descriptionTextView.startAnimation(fadeIn);
        btnLogin.startAnimation(slideIn);
        btnRegister.startAnimation(slideIn);

        // Action pour le bouton Login
        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(homeActivity.this, LoginActivity.class);
                startActivity(intent);
                overridePendingTransition(android.R.anim.slide_in_left, android.R.anim.slide_out_right); // Transition animation
            }
        });

        // Action pour le bouton Register
        btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(homeActivity.this, RegisterActivity.class);
                startActivity(intent);
                overridePendingTransition(android.R.anim.slide_in_left, android.R.anim.slide_out_right); // Transition animation
            }
        });
    }
}

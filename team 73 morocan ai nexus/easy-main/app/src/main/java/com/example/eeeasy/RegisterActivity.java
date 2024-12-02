package com.example.eeeasy;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.view.animation.AlphaAnimation;  // Import AlphaAnimation
import android.view.animation.TranslateAnimation;  // Import TranslateAnimation
import android.view.animation.Animation;    // Import Animation

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class RegisterActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        // Activer la gestion des insets (pour les marges système)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Afficher un message Toast pour tester
        Toast.makeText(this, "Register Activity Opened!", Toast.LENGTH_SHORT).show();

        // Appeler la méthode pour les animations
        fadeInAndSlideInViews();

        // Récupérer le TextView par son ID
        TextView loginLinkText = findViewById(R.id.loginLink);

        // Ajouter un OnClickListener pour détecter le clic
        loginLinkText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Créer une intention pour ouvrir l'activité de connexion
                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
                startActivity(intent); // Lancer l'activité
            }
        });
    }

    private void fadeInAndSlideInViews() {
        // Créer une animation de fade-in et glissement pour le logo
        ImageView logoImageView = findViewById(R.id.logoImageView);
        AlphaAnimation logoFadeIn = new AlphaAnimation(0f, 1f); // Fade from transparent to visible
        logoFadeIn.setDuration(1000); // Durée de l'animation

        TranslateAnimation logoSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f, // Glisser depuis la gauche
                Animation.RELATIVE_TO_PARENT, 0f,  // Atteindre la position d'origine
                Animation.RELATIVE_TO_PARENT, 0f,  // Pas de mouvement vertical
                Animation.RELATIVE_TO_PARENT, 0f
        );
        logoSlideIn.setDuration(1000); // Durée de l'animation

        logoImageView.startAnimation(logoFadeIn);
        logoImageView.startAnimation(logoSlideIn);

        // Créer une animation de fade-in et glissement pour le texte de bienvenue
        TextView welcomeText = findViewById(R.id.registerTitle);
        AlphaAnimation welcomeFadeIn = new AlphaAnimation(0f, 1f);
        welcomeFadeIn.setDuration(1000);
        welcomeFadeIn.setStartOffset(500); // Delay before starting the fade-in

        TranslateAnimation welcomeSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f, // Glissement depuis la gauche
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        welcomeSlideIn.setDuration(1000);
        welcomeSlideIn.setStartOffset(500); // Delay before starting the slide-in

        welcomeText.startAnimation(welcomeFadeIn);
        welcomeText.startAnimation(welcomeSlideIn);

        // Créer une animation de fade-in et glissement pour le champ Full Name
        EditText fullNameEditText = findViewById(R.id.fullNameEditText);
        AlphaAnimation fullNameFadeIn = new AlphaAnimation(0f, 1f);
        fullNameFadeIn.setDuration(1000);
        fullNameFadeIn.setStartOffset(1000); // Delay before starting the fade-in

        TranslateAnimation fullNameSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        fullNameSlideIn.setDuration(1000);
        fullNameSlideIn.setStartOffset(1000); // Delay before starting the slide-in

        fullNameEditText.startAnimation(fullNameFadeIn);
        fullNameEditText.startAnimation(fullNameSlideIn);

        // Créer une animation de fade-in et glissement pour le champ Email
        EditText emailEditText = findViewById(R.id.emailEditText);
        AlphaAnimation emailFadeIn = new AlphaAnimation(0f, 1f);
        emailFadeIn.setDuration(1000);
        emailFadeIn.setStartOffset(1500); // Delay before starting the fade-in

        TranslateAnimation emailSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        emailSlideIn.setDuration(1000);
        emailSlideIn.setStartOffset(1500); // Delay before starting the slide-in

        emailEditText.startAnimation(emailFadeIn);
        emailEditText.startAnimation(emailSlideIn);

        // Créer une animation de fade-in et glissement pour le champ Password
        EditText passwordEditText = findViewById(R.id.passwordEditText);
        AlphaAnimation passwordFadeIn = new AlphaAnimation(0f, 1f);
        passwordFadeIn.setDuration(1000);
        passwordFadeIn.setStartOffset(2000); // Delay before starting the fade-in

        TranslateAnimation passwordSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        passwordSlideIn.setDuration(1000);
        passwordSlideIn.setStartOffset(2000); // Delay before starting the slide-in

        passwordEditText.startAnimation(passwordFadeIn);
        passwordEditText.startAnimation(passwordSlideIn);

        // Créer une animation de fade-in et glissement pour le champ Confirm Password
        EditText confirmPasswordEditText = findViewById(R.id.confirmPasswordEditText);
        AlphaAnimation confirmPasswordFadeIn = new AlphaAnimation(0f, 1f);
        confirmPasswordFadeIn.setDuration(1000);
        confirmPasswordFadeIn.setStartOffset(2500); // Delay before starting the fade-in

        TranslateAnimation confirmPasswordSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        confirmPasswordSlideIn.setDuration(1000);
        confirmPasswordSlideIn.setStartOffset(2500); // Delay before starting the slide-in

        confirmPasswordEditText.startAnimation(confirmPasswordFadeIn);
        confirmPasswordEditText.startAnimation(confirmPasswordSlideIn);

        // Créer une animation pour le bouton Register
        Button registerButton = findViewById(R.id.btnRegister);
        AlphaAnimation registerFadeIn = new AlphaAnimation(0f, 1f);
        registerFadeIn.setDuration(1000);
        registerFadeIn.setStartOffset(3000); // Delay before starting the fade-in

        TranslateAnimation registerSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        registerSlideIn.setDuration(1000);
        registerSlideIn.setStartOffset(3000); // Delay before starting the slide-in

        registerButton.startAnimation(registerFadeIn);
        registerButton.startAnimation(registerSlideIn);
    }
}

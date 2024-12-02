package com.example.eeeasy;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.Button;
import android.widget.EditText;
import android.content.Intent;
import android.widget.ImageView;
import android.view.animation.AlphaAnimation;  // Import AlphaAnimation
import android.view.animation.TranslateAnimation;  // Import TranslateAnimation
import android.view.animation.Animation;    // Import Animation

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Activer la gestion des insets (pour les marges système)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        // Référence au bouton Logi n
        Button btnLogin = findViewById(R.id.btnLogin);

//        // Action au clic sur le bouton Login
//        btnLogin.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                // Démarrer AccueilMainActivity
//                Intent intent = new Intent(LoginActivity.this, AccueilMainActivity.class);
//                startActivity(intent);
//                // Optionnel : Fermer LoginActivity si nécessaire
//                finish();
//            }
//        });

        // Afficher un message Toast pour tester
        Toast.makeText(this, "Login Activity Opened!", Toast.LENGTH_SHORT).show();

        // Simple fade-in animation with slide-in effect
        fadeInAndSlideInViews();

        // Récupérer le TextView par son ID
        TextView registerLinkText = findViewById(R.id.registerLinkText);

        // Ajouter un OnClickListener pour détecter le clic
        registerLinkText.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Créer une intention pour ouvrir l'activité de connexion
                Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(intent); // Lancer l'activité
            }
        });
    }

    private void fadeInAndSlideInViews() {
        // Créer une animation de fade-in et glissement à gauche pour le logo
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
        TextView welcomeText = findViewById(R.id.loginWelcomeText);
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

        // Créer une animation de fade-in et glissement pour le champ Email
        EditText emailEditText = findViewById(R.id.emailEditText);
        AlphaAnimation emailFadeIn = new AlphaAnimation(0f, 1f);
        emailFadeIn.setDuration(1000);
        emailFadeIn.setStartOffset(1000); // Delay before starting the fade-in

        TranslateAnimation emailSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        emailSlideIn.setDuration(1000);
        emailSlideIn.setStartOffset(1000); // Delay before starting the slide-in

        emailEditText.startAnimation(emailFadeIn);
        emailEditText.startAnimation(emailSlideIn);

        // Créer une animation de fade-in et glissement pour le champ Password
        EditText passwordEditText = findViewById(R.id.passwordEditText);
        AlphaAnimation passwordFadeIn = new AlphaAnimation(0f, 1f);
        passwordFadeIn.setDuration(1000);
        passwordFadeIn.setStartOffset(1500); // Delay before starting the fade-in

        TranslateAnimation passwordSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        passwordSlideIn.setDuration(1000);
        passwordSlideIn.setStartOffset(1500); // Delay before starting the slide-in

        passwordEditText.startAnimation(passwordFadeIn);
        passwordEditText.startAnimation(passwordSlideIn);

        // Créer une animation de fade-in et glissement pour le bouton de connexion
        Button loginButton = findViewById(R.id.btnLogin);
        AlphaAnimation loginButtonFadeIn = new AlphaAnimation(0f, 1f);
        loginButtonFadeIn.setDuration(1000);
        loginButtonFadeIn.setStartOffset(2000); // Delay before starting the fade-in

        TranslateAnimation loginButtonSlideIn = new TranslateAnimation(
                Animation.RELATIVE_TO_PARENT, -1f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f,
                Animation.RELATIVE_TO_PARENT, 0f
        );
        loginButtonSlideIn.setDuration(1000);
        loginButtonSlideIn.setStartOffset(2000); // Delay before starting the slide-in

        loginButton.startAnimation(loginButtonFadeIn);
        loginButton.startAnimation(loginButtonSlideIn);
        // Initialisation du bouton Login
        loginButton = findViewById(R.id.btnLogin);

        // Ajouter un OnClickListener
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Redirection vers homeActivity2
                Intent intent = new Intent(LoginActivity.this, homeActivity2.class);
                startActivity(intent);
            }
        });
    }
}

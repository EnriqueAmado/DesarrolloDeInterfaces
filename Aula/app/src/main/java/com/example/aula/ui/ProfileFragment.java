package com.example.aula.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatDelegate;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.aula.R;
import com.example.aula.viewmodel.ProfileViewModel;
import com.google.android.material.materialswitch.MaterialSwitch;

public class ProfileFragment extends Fragment {

    private ProfileViewModel vModel;
    private TextView tvUid;
    private MaterialSwitch swDark;

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_profile, container, false);

        tvUid = root.findViewById(R.id.tvIdUsuario);
        swDark = root.findViewById(R.id.swModoOscuro);
        vModel = new ViewModelProvider(this).get(ProfileViewModel.class);

        // 1. Mostrar ID
        String idReal = com.google.firebase.auth.FirebaseAuth.getInstance().getUid();
        vModel.cargarDatos(idReal);

        vModel.getUid().observe(getViewLifecycleOwner(), s -> {
            tvUid.setText(s);
        });

        //Modo Oscuro
        swDark.setOnCheckedChangeListener((button, isChecked) -> {
            if (isChecked) {
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES);
            } else {
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);
            }
        });

        // 3. Cerrar Sesión
        root.findViewById(R.id.btnCerrarSesion).setOnClickListener(v -> {
            com.google.firebase.auth.FirebaseAuth.getInstance().signOut();
        });

        return root;
    }
}

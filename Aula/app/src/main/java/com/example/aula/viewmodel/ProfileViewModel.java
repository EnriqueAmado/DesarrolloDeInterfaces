package com.example.aula.viewmodel;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class ProfileViewModel extends ViewModel {
    private MutableLiveData<String> uid = new MutableLiveData<>();
    public LiveData<String> getUid() {
        return uid;
    }

    // Método para cargar el ID desde Firebase
    public void cargarDatos(String firebaseId) {
        uid.setValue(firebaseId);
    }
}
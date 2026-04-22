package com.misitioweb.miappnotas.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.misitioweb.miappnotas.data.local.Nota
import com.misitioweb.miappnotas.data.repository.NotaRepositorio
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class NotaViewModel(
    private val repositorio: NotaRepositorio
) : ViewModel() {

    val notas: StateFlow<List<Nota>> = repositorio.todasLasNotas
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    private val _notaSeleccionada = MutableStateFlow<Nota?>(null)
    val notaSeleccionada: StateFlow<Nota?> = _notaSeleccionada.asStateFlow()

    private val _mostrarEditor = MutableStateFlow(false)
    val mostrarEditor: StateFlow<Boolean> = _mostrarEditor.asStateFlow()

    fun seleccionarNota(nota: Nota?) {
        _notaSeleccionada.value = nota
        _mostrarEditor.value = nota != null
    }

    fun nuevaNota() {
        _notaSeleccionada.value = null
        _mostrarEditor.value = true
    }

    fun guardarNota(nota: Nota) {
        viewModelScope.launch {
            if (nota.id == 0L) {
                repositorio.insertar(nota)
            } else {
                repositorio.actualizar(nota)
            }
            cerrarEditor()
        }
    }

    fun eliminarNota(nota: Nota) {
        viewModelScope.launch {
            repositorio.eliminar(nota)
            cerrarEditor()
        }
    }

    fun cerrarEditor() {
        _notaSeleccionada.value = null
        _mostrarEditor.value = false
    }

    class Factory(private val repositorio: NotaRepositorio) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(NotaViewModel::class.java)) {
                return NotaViewModel(repositorio) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
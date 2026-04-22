package com.misitioweb.miappnotas

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.misitioweb.miappnotas.data.local.NotaDatabase
import com.misitioweb.miappnotas.data.repository.NotaRepositorio
import com.misitioweb.miappnotas.ui.NotaViewModel
import com.misitioweb.miappnotas.ui.screens.EditarNotaScreen
import com.misitioweb.miappnotas.ui.screens.ListaNotasScreen
import com.misitioweb.miappnotas.ui.theme.MiAppNotasTheme

class MainActivity : ComponentActivity() {

    private lateinit var repositorio: NotaRepositorio

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val database = NotaDatabase.obtener(applicationContext)
        repositorio = NotaRepositorio(database.notaDao())

        enableEdgeToEdge()
        setContent {
            MiAppNotasTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val viewModel: NotaViewModel = viewModel(
                        factory = NotaViewModel.Factory(repositorio)
                    )

                    val notas by viewModel.notas.collectAsState()
                    val notaSeleccionada by viewModel.notaSeleccionada.collectAsState()
                    val mostrarEditor by viewModel.mostrarEditor.collectAsState()

                    if (mostrarEditor) {
                        EditarNotaScreen(
                            nota = notaSeleccionada,
                            onGuardar = { viewModel.guardarNota(it) },
                            onEliminar = { viewModel.eliminarNota(it) },
                            onVolver = { viewModel.cerrarEditor() }
                        )
                    } else {
                        ListaNotasScreen(
                            notas = notas,
                            onNotaClick = { viewModel.seleccionarNota(it) },
                            onAgregarClick = { viewModel.nuevaNota() },
                            onEliminarClick = { viewModel.eliminarNota(it) }
                        )
                    }
                }
            }
        }
    }
}
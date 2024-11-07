package uy.edu.um;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProcesadorDePagoTest {

    @Test
    public void testProcesarPago() {
        ProcesadorDePago procesador = new ProcesadorDePago();
        Pedido pedido = new Pedido(1, 1);
        assertDoesNotThrow(() -> procesador.procesarPago(pedido));
    }
}

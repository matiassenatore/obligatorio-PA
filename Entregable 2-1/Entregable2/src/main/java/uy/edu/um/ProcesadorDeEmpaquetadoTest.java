package uy.edu.um;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProcesadorDeEmpaquetadoTest {

    @Test
    public void testEmpacarPedido() {
        ProcesadorDeEmpaquetado procesador = new ProcesadorDeEmpaquetado();
        Pedido pedido = new Pedido(1, 1);
        assertDoesNotThrow(() -> procesador.empacarPedido(pedido));
    }
}

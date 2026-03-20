package xyz.tinyhuman.sdk;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class TinyHumanErrorTest {

    @Test
    void constructorSetsFields() {
        TinyHumanError err = new TinyHumanError("bad request", 400, Map.of("error", "bad"));
        assertEquals("bad request", err.getMessage());
        assertEquals(400, err.getStatus());
        assertEquals(Map.of("error", "bad"), err.getBody());
    }

    @Test
    void constructorWithoutBody() {
        TinyHumanError err = new TinyHumanError("not found", 404);
        assertEquals("not found", err.getMessage());
        assertEquals(404, err.getStatus());
        assertNull(err.getBody());
    }

    @Test
    void isRuntimeException() {
        TinyHumanError err = new TinyHumanError("fail", 500);
        assertInstanceOf(RuntimeException.class, err);
    }
}

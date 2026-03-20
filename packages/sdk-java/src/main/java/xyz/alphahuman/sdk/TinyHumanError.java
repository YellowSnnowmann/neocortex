package xyz.tinyhuman.sdk;

/**
 * Thrown when the TinyHuman API returns a non-2xx response or a non-JSON body.
 */
public class TinyHumanError extends RuntimeException {

    private final int status;
    private final Object body;

    public TinyHumanError(String message, int status, Object body) {
        super(message);
        this.status = status;
        this.body = body;
    }

    public TinyHumanError(String message, int status) {
        this(message, status, null);
    }

    public int getStatus() {
        return status;
    }

    public Object getBody() {
        return body;
    }
}

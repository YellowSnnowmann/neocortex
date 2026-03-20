namespace TinyHuman.Sdk;

public class TinyHumanError : Exception
{
    public int Status { get; }
    public string Body { get; }

    public TinyHumanError(string message, int status, string body)
        : base(message)
    {
        Status = status;
        Body = body;
    }
}

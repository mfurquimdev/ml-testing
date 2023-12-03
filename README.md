# Testdome


## Using Typer CLI
Make requests with `sample request` command.  
Take a look at `sample run_me` command at [src/cli/sample/main.py](src/cli/sample/main.py) for more useful Typer features.

```bash
pdm cli sample --verbose run_me Larissa --lie --network simplE --location src/cli/sample/main.py -e
pdm cli sample request
pdm cli request tracks
```


## Make request on server

The `http` command from [httpie](https://github.com/httpie/cli) is an optional but useful tool for testing.

These GET requests are equivalent:
```bash
curl --request GET "http://localhost:44681/sample/1?name=asd"
http GET :44681/sample/1 name=='asd'
```

As are these POST requests:
```bash
curl --request POST \
    --header 'accept: application/json' \
    --header 'Content-Type: application/json' \
    --data '{"num": 2, "name": "lkj"}' \
    "http://localhost:44681/train?name=asd&num=1"

http --json POST :44681/train num==1 name=='asd' num:=2 name="lkj"
```


# Installing and using vagrant for OpenDiscovery

Vagrant is a tool which is used to develop complete and reproducable computational environments. I have created an environment (or a **box** in vagrant terminology), which has OpenDiscovery, Open Babel, Vina, and AmberTools installed. This box can be downloaded (by you!) and set up to perfectly mimic a fully functional system to use OpenDiscovery. 

## Installing
Instlling Vagrant is easy. Simple go to [this page](https://www.vagrantup.com/downloads.html), download the applicable installer and follow the installation dialogs.

You will also need [VirtualBox](https://www.virtualbox.org/wiki/Downloads). Like Vagrant, download and install like a normal application.

You can check if these are install properly by typing the following in terminal:

```bash
vagrant --version
```

## Downloading the OD Box
Downloading the [OD environment](https://atlas.hashicorp.com/garethprice/boxes/opendiscovery) is also simple:

```bash
# create a new folder in your home directory
cd ~ && mkdir vagrant-od && cd ~/vagrant-od
vagrant init garethprice/opendiscovery
```

This will download a 1.4 GB file, so depending on your internet speed this may take a while.

## Using the OD Box
Make sure you are in the directory you made before (`cd ~/vagrant-od), then run the following in terminal:

```bash
vagrant up --provider virtualbox
```

This will cause the box to boot up and start running. To login you simple type:

```bash
vagrant ssh
```

Vagrant will log you in to the box. It will symlink the folder you're in (`~/vagrant-od`) to `\vagrant` in the box. So any files you put in vagrant-od will be usable in the OD box. 

Then, all you need to do is set up your folders and files, put them into `~/vagrant-od`, and run `odscreen` like usual.

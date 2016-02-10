Assignment 1 in IIIT-H, course Computer Networks. Prof Ganesh Iyer, Spring 2016
==

Aim:
----
To create an application level file sharing protocol with support for download and upload for files and indexed searching

Features:
---
1. The system should have 2 clients (acting as servers simultaniously) listening to the communication channel for requests and waiting to share files (avoiding collisions) using an application layer protocol (like FTP/HTTP). 

2. Each client has the ability to do the following:
    a. Know the files present on each other machines in the designated shared folders.
    b. Download the files from the shared folder.

3. The system should perodically check for any changes made to the shared folders.

4. File transfer should incorporate MD5checksums to handle file transfer errors.

Specifications:
---
The system should incorporate the following commands:

1. IndexGet flag (args)\
    a. can request the display of the shared files on the connnected system.
    b. The history of requests made by either clients should be maintained at each of the clients respecitvely.
    c. the flag variable can be shortlist, longlist, regex
        1) shortlist:
            flag would mean that the client only wants to know the names of the files between a specific set of timestamps. The sample query is below
            $>IndexGet shortlist <starttimestamp> <endtimestamp>
            Output : should include 'name' 'size' 'timestamp' 'type of file'
        2) longlist:
            Flag would mean that client wants to know the entire listing of the shared folders/directory including shortlist options.

2. FileHash flag (args):
This commmand indicates that the client wants to check if any of the files on the other end have been changed. The flag variable can take two values, verify and checkall
    1) verify: flag should check for the specific file name provided as command line argument and return its 'checksum' and 'lastmodified' timestamp.
    $> FileHash verify <filename>
    Output: Checksum and lastmodified timestamp of the file

    2) checkall: Flag should check perform what 'verify' does for all the files in the shared folder.
(This can be used to periodically check the files)

3. FileDownload flag (args):
As the name suggests, would be the command to download the files from the shared folder of the connected user to our shared folder.
    a. the flag variable can take the value TCP or UDP depending on the user request.
    b. if the socket is not available, it should created and both clients must use this socket for file transfer.
        $> FileDownload <filename>
        Output: should contain the filename, filesize, lastmodified, timestamp and the MD5checksum of the file.
(HINT: the filesize parameter might be used to allocate memory)

******

The assignment will be done in CPP. This assignment is a building block for bluetooth programming.

Done by:
Shaleen Garg

email: shaleen.garg@students.iiit.ac.in
